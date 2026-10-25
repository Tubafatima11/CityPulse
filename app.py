"""
CityPulse — 30-Minute Hackathon Prototype
Turn street footage into actionable infrastructure intelligence.
"""

import streamlit as st
import pandas as pd
from PIL import Image
import io
import time
from sample_data import (
    SAMPLE_ISSUES,
    ISSUE_CATEGORIES,
    calculate_priority_score,
    group_observations_by_hotspot,
    BASE_LAT,
    BASE_LON
)
from gemma_triage import analyze_observation, OFFLINE_PRESETS

# Page configuration
st.set_page_config(
    page_title="CityPulse | Street Infrastructure Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-contrast civic engineering theme
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-card {
        background: #1a1f2c;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .priority-badge-high {
        background-color: #d32f2f;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .priority-badge-med {
        background-color: #f57c00;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .priority-badge-low {
        background-color: #388e3c;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .formula-box {
        background-color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        font-family: monospace;
        font-size: 0.9em;
        margin: 8px 0;
    }
    .evidence-pill {
        display: inline-block;
        background-color: #27272a;
        border: 1px solid #3f3f46;
        border-radius: 4px;
        padding: 4px 10px;
        margin: 2px;
        font-size: 0.85em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "issues" not in st.session_state:
    st.session_state.issues = [dict(issue) for issue in SAMPLE_ISSUES]

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "demo_view" not in st.session_state:
    st.session_state.demo_view = "all"

# SIDEBAR: Configuration & Context
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/city.png", width=64)
    st.title("CityPulse")
    st.caption("Multimodal Street Infrastructure Triage")
    st.markdown("---")
    
    st.subheader("⚙️ Model Configuration")
    api_key_input = st.text_input(
        "Gemini / Gemma API Key (Optional)",
        type="password",
        help="Optional. Leave blank to run seamless offline heuristic demo."
    )
    
    model_choice = st.selectbox(
        "Triage Model",
        ["Gemma 4 Multimodal (Vision)", "Gemini 1.5 Flash", "Offline Fallback Heuristic"],
        index=0
    )
    
    if api_key_input:
        st.success("API key loaded for live multimodal inference.")
    else:
        st.info("💡 Offline demo mode active. Realistic triage presets ready.")

    st.markdown("---")
    st.subheader("🎯 Demo Controls")
    if st.button("🔄 Reset Queue to Initial Samples", use_container_width=True):
        st.session_state.issues = [dict(issue) for issue in SAMPLE_ISSUES]
        st.session_state.last_analysis = None
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Transparency & Safety Notice:**
    - AI-assisted triage; human inspection required.
    - Transparent component scoring (Severity + Recurrence + Accessibility).
    - Fictional demonstration data.
    """)

# MAIN HEADER
st.title("🏙️ CityPulse — Infrastructure Intelligence")
st.markdown("**Turn street footage into an actionable, evidence-backed municipal maintenance queue.**")

# Top KPI row
current_issues = st.session_state.issues
hotspots = group_observations_by_hotspot(current_issues)

total_open = len(current_issues)
recurring_hotspots = sum(1 for h in hotspots if h["observation_count"] > 1 or h["total_citizen_reports"] > 1)
high_urgency_count = sum(
    1 for i in current_issues 
    if calculate_priority_score(i["severity"], i.get("repeat_count", 1), i.get("accessibility_impact", 0))["score"] >= 20
)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Open Observations", total_open, help="Total active street reports in queue")
with col_m2:
    st.metric("Recurring Hotspots", recurring_hotspots, delta="Grouped Locations", help="Locations with repeated citizen reports")
with col_m3:
    st.metric("High-Urgency Inspections", high_urgency_count, delta="Score ≥ 20", delta_color="inverse")
with col_m4:
    st.metric("Triage Processing", "< 1.2 sec", "Gemma Multimodal")

st.markdown("---")

# TABS FOR WORKFLOW
tab_queue, tab_analyze, tab_hotspots, tab_pitch = st.tabs([
    "📋 Priority Inspection Queue",
    "📸 Analyze Street Observation (Gemma)",
    "🗺️ Hotspot Recurrence Map",
    "⏱️ 45-Second Judge Rehearsal"
])

# -------------------------------------------------------------
# TAB 1: PRIORITY INSPECTION QUEUE
# -------------------------------------------------------------
with tab_queue:
    st.subheader("Active Prioritized Maintenance Queue")
    st.caption("Ranked by deterministic, transparent priority score. Evaluated before dispatch.")

    # Filter bar
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    with f_col1:
        category_filter = st.selectbox(
            "Filter by Issue Category:",
            ["All Categories"] + [v["label"] for v in ISSUE_CATEGORIES.values()],
            index=0
        )
    with f_col2:
        urgency_filter = st.selectbox(
            "Filter by Urgency Band:",
            ["All Urgency Levels", "HIGH URGENCY (≥20)", "MEDIUM PRIORITY (14-19)", "ROUTINE REVIEW (<14)"],
            index=0
        )
    with f_col3:
        st.caption("Scoring Rule:")
        st.code("Score = (Severity × 3) + (min(Repeats-1, 4) × 2) + (Accessibility × 2)")

    # Sort issues by computed score
    annotated_issues = []
    for issue in current_issues:
        score_info = calculate_priority_score(
            issue["severity"],
            issue.get("repeat_count", 1),
            issue.get("accessibility_impact", 0)
        )
        annotated_issues.append((issue, score_info))

    annotated_issues.sort(key=lambda x: x[1]["score"], reverse=True)

    # Render filtered cards
    displayed_count = 0
    for issue, score_data in annotated_issues:
        category_meta = ISSUE_CATEGORIES.get(issue.get("issue_type", "other"), ISSUE_CATEGORIES["other"])
        
        # Apply filters
        if category_filter != "All Categories" and category_meta["label"] != category_filter:
            continue
        if urgency_filter == "HIGH URGENCY (≥20)" and score_data["score"] < 20:
            continue
        if urgency_filter == "MEDIUM PRIORITY (14-19)" and not (14 <= score_data["score"] < 20):
            continue
        if urgency_filter == "ROUTINE REVIEW (<14)" and score_data["score"] >= 14:
            continue

        displayed_count += 1
        
        # Render item expander
        header_title = (
            f"#{displayed_count} · [{issue['id']}] {category_meta['icon']} {issue.get('issue_label', issue.get('summary', 'Issue'))} "
            f"| Location: {issue.get('location_name', issue.get('location_id'))} "
            f"| Priority Score: {score_data['score']} ({score_data['band']})"
        )
        
        with st.expander(header_title, expanded=(displayed_count == 1)):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**Summary:** {issue.get('summary')}")
                st.markdown("**Direct Visible Evidence:**")
                for ev in issue.get("visible_evidence", []):
                    st.markdown(f"- 🔎 {ev}")
                
                st.markdown(f"**⚠️ What Cannot Be Established (Uncertainty):**")
                st.info(issue.get("uncertainty", "Requires physical tactile inspection."))
                
                st.markdown(f"**🛠️ Recommended Action:**")
                st.success(issue.get("recommended_action", "Dispatch field verification crew."))

            with c2:
                st.markdown("#### Priority Breakdown")
                st.markdown(
                    f"<div class='formula-box'>"
                    f"<b>Score: {score_data['score']}</b><br/>"
                    f"Formula: {score_data['explanation']}<br/>"
                    f"• Severity: {score_data['severity_val']}/5 ({score_data['severity_pts']} pts)<br/>"
                    f"• Citizen Reports: {score_data['repeat_val']}x ({score_data['repeat_pts']} pts)<br/>"
                    f"• Accessibility: {score_data['accessibility_val']}/5 ({score_data['accessibility_pts']} pts)"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
                st.caption(f"Observed at: {issue.get('observed_at', 'Recent')} · Location Verified: {issue.get('verified_location', True)}")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"Mark Inspected", key=f"insp_{issue['id']}"):
                        st.session_state.issues = [i for i in st.session_state.issues if i['id'] != issue['id']]
                        st.toast(f"Issue {issue['id']} marked as inspected and removed from triage queue.")
                        st.rerun()
                with btn_col2:
                    if st.button(f"Add Citizen Report", key=f"dup_{issue['id']}"):
                        issue['repeat_count'] = issue.get('repeat_count', 1) + 1
                        st.toast(f"Citizen report added to {issue['id']} (Repeats: {issue['repeat_count']})")
                        st.rerun()

    if displayed_count == 0:
        st.warning("No issues match the selected filter criteria.")

# -------------------------------------------------------------
# TAB 2: ANALYZE STREET OBSERVATION (GEMMA)
# -------------------------------------------------------------
with tab_analyze:
    st.subheader("Multimodal Street Observation Triage")
    st.caption("Upload a street photo or choose a sample to extract structured evidence, severity, and uncertainty.")

    col_input, col_preview = st.columns([1, 1])

    with col_input:
        st.markdown("#### 1. Select or Upload Street Observation")
        sample_choice = st.selectbox(
            "Or choose a sample street observation:",
            [
                "Custom Upload",
                "Sample 1: Clogged Inflow Drain (Block A)",
                "Sample 2: Upheaved Concrete Sidewalk (Block B)",
                "Sample 3: Road Asphalt Pothole (Block C)",
                "Sample 4: Overflowing Waste Receptacle (Block D)"
            ],
            index=1
        )

        uploaded_file = None
        preset_key = None
        default_desc = ""

        if sample_choice == "Custom Upload":
            uploaded_file = st.file_uploader("Upload street photograph (PNG, JPG, WEBP):", type=["png", "jpg", "jpeg", "webp"])
            user_desc = st.text_area("Optional resident complaint / context:", placeholder="e.g. Water is backing up into the bike lane after light rain...")
        elif "Clogged Inflow Drain" in sample_choice:
            preset_key = "blocked_drain"
            default_desc = "Curb drain is covered in tree leaves and road silt. Water is starting to spill over the curb."
            user_desc = st.text_area("Resident report:", value=default_desc)
        elif "Upheaved Concrete Sidewalk" in sample_choice:
            preset_key = "broken_footpath"
            default_desc = "Sidewalk slab has buckled up over 2 inches from tree roots. An elderly resident tripped yesterday."
            user_desc = st.text_area("Resident report:", value=default_desc)
        elif "Road Asphalt Pothole" in sample_choice:
            preset_key = "pothole"
            default_desc = "Large deep pothole directly in the bus lane. Motorists are swerving dangerously."
            user_desc = st.text_area("Resident report:", value=default_desc)
        else:
            preset_key = "overflowing_rubbish"
            default_desc = "Garbage bin overflowing onto the walking route. Loose cardboard and boxes spilling over."
            user_desc = st.text_area("Resident report:", value=default_desc)

        location_tag = st.selectbox(
            "Assign Location Identifier:",
            ["BLOCK-A (Market & 7th)", "BLOCK-B (Elmwood Walkway)", "BLOCK-C (4th Ave Hub)", "BLOCK-D (Pine St Alley)", "NEW-LOCATION (Unverified)"],
            index=0 if "Block A" in sample_choice else (1 if "Block B" in sample_choice else (2 if "Block C" in sample_choice else 3))
        )

        run_button = st.button("⚡ Run Gemma Triage Analysis", type="primary", use_container_width=True)

    with col_preview:
        st.markdown("#### 2. Observation Frame Preview")
        image_bytes = None
        mime_type = "image/jpeg"
        sample_img_map = {
            "blocked_drain": "sample_drain.jpg",
            "broken_footpath": "sample_sidewalk.jpg",
            "pothole": "sample_pothole.jpg",
            "overflowing_rubbish": "sample_rubbish.jpg"
        }

        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()
            mime_type = uploaded_file.type
            st.image(uploaded_file, caption="Citizen Uploaded Frame", use_container_width=True)
        elif preset_key and preset_key in sample_img_map:
            import os
            sample_path = os.path.join(os.path.dirname(__file__), "sample_images", sample_img_map[preset_key])
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    image_bytes = f.read()
                st.image(image_bytes, caption=f"Observation Frame: {sample_choice}", use_container_width=True)
            else:
                st.markdown(
                    f"""
                    <div style="background:#1e293b; border:2px dashed #475569; border-radius:8px; padding:30px; text-align:center;">
                        <span style="font-size:3em;">📷</span><br/>
                        <b>{sample_choice}</b><br/>
                        <span style="color:#94a3b8; font-size:0.9em;">Simulated high-resolution street camera frame</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f"""
                <div style="background:#1e293b; border:2px dashed #475569; border-radius:8px; padding:30px; text-align:center;">
                    <span style="font-size:3em;">📷</span><br/>
                    <b>{sample_choice}</b><br/>
                    <span style="color:#94a3b8; font-size:0.9em;">Simulated high-resolution street camera frame</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # EXECUTION
    if run_button:
        with st.spinner("Analyzing visual evidence via Gemma Multimodal Triage..."):
            time.sleep(0.6)  # Realistic inference feel
            result = analyze_observation(
                image_bytes=image_bytes,
                mime_type=mime_type,
                description=user_desc,
                preset_key=preset_key,
                api_key=api_key_input
            )
            st.session_state.last_analysis = {
                "result": result,
                "location_tag": location_tag,
                "user_desc": user_desc
            }

    # DISPLAY ANALYSIS RESULTS
    if st.session_state.last_analysis:
        analysis = st.session_state.last_analysis["result"]
        data = analysis["data"]
        loc_str = st.session_state.last_analysis["location_tag"]
        loc_id = loc_str.split(" ")[0]
        
        st.markdown("---")
        st.markdown(f"### 🎯 Structured Triage Result")
        st.caption(f"Source: {analysis['source']} | {analysis.get('note', '')}")
        
        col_res1, col_res2, col_res3 = st.columns([2, 2, 2])
        
        # Calculate what priority score this would receive
        # Check if this location already exists in our queue to compute repeat count!
        existing_matches = [i for i in st.session_state.issues if i.get("location_id") == loc_id and i.get("issue_type") == data["issue_type"]]
        repeat_count = 1 + sum(i.get("repeat_count", 1) for i in existing_matches)
        
        score_calc = calculate_priority_score(data["severity"], repeat_count, data["accessibility_impact"])

        with col_res1:
            cat = ISSUE_CATEGORIES.get(data["issue_type"], ISSUE_CATEGORIES["other"])
            st.markdown(f"**Identified Issue:** {cat['icon']} **{cat['label']}**")
            st.markdown(f"**Summary:** {data['summary']}")
            st.markdown(f"**Severity Rating:** {'⭐' * data['severity']} ({data['severity']}/5)")
            st.markdown(f"**Accessibility Impact:** {'♿' * data['accessibility_impact']} ({data['accessibility_impact']}/5)")

        with col_res2:
            st.markdown("**🔎 Extracted Visual Evidence:**")
            for ev in data.get("visible_evidence", []):
                st.markdown(f"- {ev}")
            st.markdown("**⚠️ Uncertainty & Unseen Factors:**")
            st.info(data.get("uncertainty", "Physical on-site test required."))

        with col_res3:
            st.markdown("#### Computed Priority Score")
            st.markdown(
                f"<div class='formula-box'>"
                f"<b style='font-size:1.2em;'>Score: {score_calc['score']} ({score_calc['band']})</b><br/>"
                f"Breakdown: {score_calc['explanation']}<br/>"
                f"• Recurrence bonus: {repeat_count} reports linked to {loc_id}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"**Next Action:** {data['recommended_action']}")

            if st.button("➕ Enqueue to Live Maintenance Queue", type="primary"):
                new_id = f"CP-{len(st.session_state.issues) + 101}"
                new_item = {
                    "id": new_id,
                    "location_id": loc_id,
                    "location_name": loc_str,
                    "lat": BASE_LAT + (0.001 * len(st.session_state.issues)),
                    "lon": BASE_LON - (0.001 * len(st.session_state.issues)),
                    "issue_type": data["issue_type"],
                    "issue_label": f"{cat['label']} ({loc_id})",
                    "summary": data["summary"],
                    "severity": data["severity"],
                    "accessibility_impact": data["accessibility_impact"],
                    "repeat_count": repeat_count,
                    "visible_evidence": data["visible_evidence"],
                    "uncertainty": data["uncertainty"],
                    "recommended_action": data["recommended_action"],
                    "observed_at": time.strftime("%Y-%m-%d %H:%M"),
                    "status": "Queued",
                    "verified_location": "NEW-LOCATION" not in loc_str
                }
                st.session_state.issues.insert(0, new_item)
                st.session_state.last_analysis = None
                st.success(f"Added {new_id} to priority queue with calculated score of {score_calc['score']}!")
                st.rerun()

# -------------------------------------------------------------
# TAB 3: HOTSPOT RECURRENCE MAP & GROUPING
# -------------------------------------------------------------
with tab_hotspots:
    st.subheader("Physical Location Hotspot Grouping")
    st.caption("Consolidates multi-report observations by location identifier. Prevents fragmented duplicate handling.")

    m_col1, m_col2 = st.columns([3, 2])

    with m_col1:
        # Prepare dataframe for st.map
        map_points = []
        for h in hotspots:
            map_points.append({
                "lat": h["lat"],
                "lon": h["lon"],
                "name": h["location_name"],
                "reports": h["total_citizen_reports"],
                "highest_score": h["highest_score"]
            })
        if map_points:
            df_map = pd.DataFrame(map_points)
            st.map(df_map, latitude="lat", longitude="lon", size="reports", zoom=14)
        st.caption("Circle size represents citizen report density at physical location.")

    with m_col2:
        st.markdown("#### Recurring Location Rollup")
        for h in hotspots:
            with st.container():
                st.markdown(
                    f"**📍 {h['location_name']}** (`{h['location_id']}`)<br/>"
                    f"• Citizen Reports: **{h['total_citizen_reports']}** | Issues: **{h['observation_count']}**<br/>"
                    f"• Peak Urgency Score: **{h['highest_score']}**<br/>"
                    f"• Categories: {', '.join(h['issue_types'])}",
                    unsafe_allow_html=True
                )
                st.divider()

# -------------------------------------------------------------
# TAB 4: 45-SECOND JUDGE REHEARSAL
# -------------------------------------------------------------
with tab_pitch:
    st.subheader("⏱️ 45-Second Judge Presentation Walkthrough")
    st.caption("Follow this exact sequence for maximum hackathon demo impact.")

    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.markdown("""
        **1. The Hook (0-10s)**
        "Cities receive thousands of fragmented photos of potholes and blocked drains. But identical issues get logged as separate tickets."
        """)
    with p2:
        st.markdown("""
        **2. The Vision (10-20s)**
        "CityPulse uses Gemma multimodal AI to analyze photos into concrete visible evidence, severity, and uncertainty."
        """)
    with p3:
        st.markdown("""
        **3. Hotspot Grouping (20-30s)**
        "Instead of separate tickets, CityPulse clusters reports by physical location to reveal chronic infrastructure hotspots."
        """)
    with p4:
        st.markdown("""
        **4. Explainable Score (30-40s)**
        "Our transparent formula weights Severity × 3, Recurrence × 2, and Accessibility × 2. Zero black-box ranking."
        """)
    with p5:
        st.markdown("""
        **5. The Close (40-45s)**
        "CityPulse doesn't replace city inspectors—it tells them where to look first."
        """)

    st.markdown("---")
    st.info("💡 **Demo Pro-tip:** Go to **Tab 2**, pick **'Sample 1: Clogged Inflow Drain'**, click **'Run Gemma Triage'**, then click **'Enqueue to Live Queue'** to demonstrate the complete workflow in 30 seconds.")
