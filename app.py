"""
CityPulse Hyderabad — GHMC Civic Connect 🏙️
AI-Powered Street Infrastructure Intelligence for Greater Hyderabad Municipal Corporation (GHMC)
Empowering Hyderabad citizens to report civic hazards and enabling municipal teams to prioritize repairs.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image
import os
import io
import time
from sample_data import (
    SAMPLE_ISSUES,
    ISSUE_CATEGORIES,
    HYDERABAD_ZONES,
    HYDERABAD_LOCALITIES,
    HYD_CENTER_LAT,
    HYD_CENTER_LON,
    calculate_priority_score,
    group_observations_by_hotspot
)
from gemma_triage import analyze_observation, OFFLINE_PRESETS

# Page configuration
st.set_page_config(
    page_title="CityPulse Hyderabad | GHMC Civic Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom civic theme styling for GHMC
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* GHMC Civic Branding Header */
    .ghmc-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%);
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Friendly cards */
    .civic-card {
        background: #151c2c;
        border: 1px solid #2a364f;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
    }
    
    .status-badge-urgent {
        background: #ef4444;
        color: white;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9em;
        display: inline-block;
    }
    
    .status-badge-med {
        background: #f59e0b;
        color: black;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9em;
        display: inline-block;
    }
    
    .status-badge-routine {
        background: #10b981;
        color: white;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9em;
        display: inline-block;
    }
    
    .evidence-item {
        background: #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 8px 14px;
        margin: 6px 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.95em;
    }
    
    .math-drawer {
        background: #0f172a;
        border: 1px solid #1e293b;
        padding: 10px 14px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.88em;
    }
    
    .map-legend-dot-red {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #ef4444;
        border-radius: 50%;
        margin-right: 6px;
    }
    .map-legend-dot-amber {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #f59e0b;
        border-radius: 50%;
        margin-right: 6px;
    }
    .map-legend-dot-green {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 6px;
    }
    
    /* Hide Streamlit default deploy button & footer */
    .stDeployButton, [data-testid="stToolbarActions"], [data-testid="stToolbar"] button:first-child {
        display: none !important;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "issues" not in st.session_state:
    st.session_state.issues = [dict(issue) for issue in SAMPLE_ISSUES]

if "last_citizen_report" not in st.session_state:
    st.session_state.last_citizen_report = None

# SIDEBAR: Configuration & Administration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/city.png", width=56)
    st.title("GHMC CityPulse")
    st.caption("Greater Hyderabad Municipal Corporation")
    st.markdown("---")
    
    st.subheader("⚙️ AI Vision Engine")
    api_key_input = st.text_input(
        "Gemini / Gemma API Key (Optional)",
        type="password",
        help="Optional. Leave blank to run offline demo with built-in Hyderabad triage presets."
    )
    if api_key_input:
        st.success("✅ Live Multimodal Vision API active")
    else:
        st.info("💡 Offline demo mode active (Instant & 100% reliable)")

    st.markdown("---")
    st.subheader("🎯 Demo Reset")
    if st.button("🔄 Reset Hyderabad Incident Queue", use_container_width=True):
        st.session_state.issues = [dict(issue) for issue in SAMPLE_ISSUES]
        st.session_state.last_citizen_report = None
        st.toast("Incidents reset to initial Hyderabad demo dataset!")
        st.rerun()

    st.markdown("---")
    st.caption("GHMC Municipal Prioritization Heuristic: Severity × 3 + Recurrence × 2 + Accessibility × 2.")

# GHMC CIVIC BRANDING BANNER
col_b1, col_b2 = st.columns([1, 10])
with col_b1:
    st.image("https://img.icons8.com/fluency/96/city.png", width=70)
with col_b2:
    st.title("🏛️ CityPulse Hyderabad — GHMC Civic Connect")
    st.markdown("**Greater Hyderabad Municipal Corporation · Public Grievance AI Triage & Hotspot Surveillance**")

# MAIN WORKFLOW TABS
tab_citizen, tab_official, tab_hotspots, tab_pitch = st.tabs([
    "📸 Citizen Corner: Click & Post Issue",
    "🏛️ GHMC Official Dashboard & Live Map",
    "📍 Hyderabad Hotspot Analytics",
    "⏱️ 45-Second Pitch & Judge Demo"
])

# ==============================================================================
# TAB 1: CITIZEN CORNER (CLICK PICTURE, ADD LOCATION, POST)
# ==============================================================================
with tab_citizen:
    st.markdown("### 📸 Report a Civic Hazard in Hyderabad")
    st.caption("See waterlogging, a dangerous pothole, broken footpath, or overflowing garbage? Click a picture, add location, and post directly to GHMC.")

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("#### 1. Capture or Select Picture")
        photo_mode = st.radio(
            "Picture source:",
            ["📸 Use Live Camera (Snap Now)", "📁 Upload from Gallery", "🧪 Test with Hyderabad Street Sample"],
            horizontal=True
        )

        image_bytes = None
        mime_type = "image/jpeg"
        preset_key = None
        auto_desc = ""

        if photo_mode == "📸 Use Live Camera (Snap Now)":
            st.info("Point your camera at the road defect or civic issue and click **Take Photo**.")
            cam_picture = st.camera_input("Snap picture of the issue")
            if cam_picture is not None:
                image_bytes = cam_picture.getvalue()
                mime_type = cam_picture.type
                st.success("✅ Picture captured successfully!")

        elif photo_mode == "📁 Upload from Gallery":
            uploaded_file = st.file_uploader(
                "Upload photo (JPG, PNG, WEBP):",
                type=["png", "jpg", "jpeg", "webp"]
            )
            if uploaded_file is not None:
                image_bytes = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                st.image(uploaded_file, caption="Selected Picture")

        else: # Sample Hyderabad Photos
            sample_choice = st.selectbox(
                "Select a sample Hyderabad street defect:",
                [
                    "Sample 1: Gachibowli Bio-Diversity Junction (Severe Storm Drain Inflow Blockage)",
                    "Sample 2: Road No. 36 Jubilee Hills (Deep Road Pothole near Metro Pillar)",
                    "Sample 3: Charminar Pedestrian Promenade (Granite Paver Displacement)",
                    "Sample 4: Kukatpally Y-Junction (Overflowing GHMC Garbage Dumper Bin)"
                ],
                index=0
            )
            sample_map = {
                "Sample 1": ("blocked_drain", "sample_drain", "Severe silt and plastic blocking catch-pit near Bio-Diversity flyover underpass. 5-inch waterlogging."),
                "Sample 2": ("pothole", "sample_pothole", "Deep jagged pothole in the fast lane under metro pillar. Motorists swerving dangerously."),
                "Sample 3": ("broken_footpath", "sample_sidewalk", "Upheaved granite slab creating trip ledge on Lad Bazaar pedestrian promenade."),
                "Sample 4": ("overflowing_rubbish", "sample_rubbish", "Community dumper bin overflowing with commercial waste onto service road shoulder.")
            }
            sample_dir = os.path.join(os.path.dirname(__file__), "sample_images")
            for k, (pkey, base_name, desc) in sample_map.items():
                if k in sample_choice:
                    preset_key = pkey
                    auto_desc = desc
                    for ext, mtype in [(".webp", "image/webp"), (".jpg", "image/jpeg"), (".jpeg", "image/jpeg"), (".png", "image/png")]:
                        target_file = os.path.join(sample_dir, base_name + ext)
                        if os.path.exists(target_file):
                            with open(target_file, "rb") as f:
                                image_bytes = f.read()
                            mime_type = mtype
                            st.image(image_bytes, caption=f"Selected: {sample_choice}")
                            break

        st.markdown("#### 2. Add Location in Hyderabad")
        location_option = st.selectbox(
            "Select locality / landmark:",
            list(HYDERABAD_LOCALITIES.keys()),
            index=0 if (preset_key == "blocked_drain") else (3 if preset_key == "pothole" else (5 if preset_key == "broken_footpath" else 7))
        )

        # Get default coordinates & zone
        def_lat, def_lon, def_zone = HYDERABAD_LOCALITIES[location_option]

        custom_landmark = ""
        if location_option == "Other / Custom Hyderabad Location":
            custom_landmark = st.text_input("Enter exact street / landmark in Hyderabad:", placeholder="e.g. Near Inorbit Mall, Mindspace, Madhapur")
            zone_selected = st.selectbox("Select GHMC Administrative Zone:", [z for z in HYDERABAD_ZONES if z != "All GHMC Zones"])
        else:
            zone_selected = def_zone
            st.caption(f"📍 **Mapped to GHMC Zone:** `{zone_selected}` · **Coordinates:** `{def_lat:.4f}° N, {def_lon:.4f}° E`")

        user_notes = st.text_area(
            "Add issue details / description (optional):",
            value=auto_desc,
            placeholder="e.g. Water is backing up into the bus lane, two-wheelers slipping...",
            help="Your note helps AI classify urgency."
        )

        submit_post_btn = st.button("🚀 Post Issue to GHMC", type="primary", use_container_width=True)

    with col_output:
        st.markdown("#### 3. AI Triage & GHMC Ticket Confirmation")
        
        if submit_post_btn:
            if image_bytes is None and not preset_key:
                st.warning("⚠️ Please snap a picture, upload an image, or choose a sample first.")
            else:
                with st.spinner("🧠 Gemma Multimodal AI is analyzing the picture for civic hazards..."):
                    time.sleep(0.5)
                    result = analyze_observation(
                        image_bytes=image_bytes,
                        mime_type=mime_type,
                        description=user_notes,
                        preset_key=preset_key,
                        api_key=api_key_input
                    )
                    
                    final_location_name = custom_landmark.strip() if custom_landmark.strip() else location_option
                    
                    # Check recurrence at this location in Hyderabad
                    existing_matches = [
                        i for i in st.session_state.issues 
                        if i.get("location_name") == final_location_name and i.get("issue_type") == result["data"]["issue_type"]
                    ]
                    repeat_count = 1 + sum(i.get("repeat_count", 1) for i in existing_matches)
                    
                    score_info = calculate_priority_score(
                        result["data"]["severity"],
                        repeat_count,
                        result["data"]["accessibility_impact"]
                    )

                    new_id = f"GHMC-{len(st.session_state.issues) + 401}"
                    new_item = {
                        "id": new_id,
                        "zone": zone_selected,
                        "ward": f"Ward {len(st.session_state.issues) * 7 + 12} - {final_location_name.split('(')[0].strip()}",
                        "location_name": final_location_name,
                        "lat": def_lat + (0.0008 * len(st.session_state.issues)),
                        "lon": def_lon - (0.0006 * len(st.session_state.issues)),
                        "issue_type": result["data"]["issue_type"],
                        "issue_label": f"{result['data']['issue_type'].replace('_', ' ').title()}",
                        "summary": result["data"]["summary"],
                        "severity": result["data"]["severity"],
                        "accessibility_impact": result["data"]["accessibility_impact"],
                        "repeat_count": repeat_count,
                        "visible_evidence": result["data"]["visible_evidence"],
                        "uncertainty": result["data"]["uncertainty"],
                        "recommended_action": result["data"]["recommended_action"],
                        "observed_at": time.strftime("%Y-%m-%d %H:%M"),
                        "status": "Logged & Prioritized",
                        "verified_location": True
                    }
                    st.session_state.issues.insert(0, new_item)
                    st.session_state.last_citizen_report = {
                        "item": new_item,
                        "score_info": score_info,
                        "source": result["source"]
                    }
                    st.toast(f"Report logged successfully! Ticket: {new_id}")

        # Display result card if report exists
        if st.session_state.last_citizen_report:
            rep = st.session_state.last_citizen_report["item"]
            sc = st.session_state.last_citizen_report["score_info"]
            cat = ISSUE_CATEGORIES.get(rep["issue_type"], ISSUE_CATEGORIES["other"])
            
            st.success("✅ **Civic Issue Posted to GHMC Successfully!**")
            
            badge_class = "status-badge-urgent" if sc["score"] >= 20 else ("status-badge-med" if sc["score"] >= 14 else "status-badge-routine")
            badge_text = f"🚨 {sc['band']}" if sc["score"] >= 20 else (f"⚠️ {sc['band']}" if sc["score"] >= 14 else f"🟢 {sc['band']}")

            st.markdown(
                f"""
                <div class="civic-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:1.3em; font-weight:bold;">{cat['icon']} {cat['label']}</span>
                        <span class="{badge_class}">{badge_text}</span>
                    </div>
                    <p><b>GHMC Ticket:</b> <code>{rep['id']}</code> | <b>Zone:</b> {rep['zone']}</p>
                    <p><b>Location:</b> 📍 {rep['location_name']}</p>
                    <p style="font-size:1.05em; color:#cbd5e1;"><b>AI Triage Summary:</b> {rep['summary']}</p>
                    <hr style="border-color:#2a364f;"/>
                    <p><b>🔎 Visible Evidence Detected by AI:</b></p>
                """,
                unsafe_allow_html=True
            )
            for ev in rep.get("visible_evidence", []):
                st.markdown(f"<div class='evidence-item'>• {ev}</div>", unsafe_allow_html=True)
            
            st.markdown(
                f"""
                    <div style="margin-top:14px;">
                        <p><b>🛠️ Assigned GHMC Action:</b> <code>{rep['recommended_action']}</code></p>
                        <p style="color:#94a3b8; font-size:0.85em;">
                            <b>Priority Score: {sc['score']} pts</b> (Severity {rep['severity']}/5 × 3 + {rep['repeat_count']} Citizen Reports + Accessibility {rep['accessibility_impact']}/5 × 2).
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("👆 Snap a picture or choose a sample on the left, add location, and click **Post Issue to GHMC** to see live AI triage.")

# ==============================================================================
# TAB 2: GHMC OFFICIAL DASHBOARD & INTERACTIVE MAP WITH INDICATIONS
# ==============================================================================
with tab_official:
    st.markdown("### 🏛️ GHMC Public Works & Maintenance Control Center")
    st.caption("Real-time citywide surveillance: prioritized inspection queue, map indications, and field crew dispatch.")

    # High-level Municipal KPIs
    hotspots = group_observations_by_hotspot(st.session_state.issues)
    critical_hazards = sum(1 for i in st.session_state.issues if calculate_priority_score(i["severity"], i.get("repeat_count", 1), i.get("accessibility_impact", 0))["score"] >= 20)
    hotspot_zones = sum(1 for h in hotspots if h["total_citizen_reports"] > 1)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Active Incidents", len(st.session_state.issues), "Across Hyderabad")
    with k2:
        st.metric("🚨 Critical Hazards (Score ≥ 20)", critical_hazards, "Requires immediate dispatch", delta_color="inverse")
    with k3:
        st.metric("📍 Multi-Report Hotspots", hotspot_zones, "Recurring citizen complaints")
    with k4:
        st.metric("Average Triage Latency", "< 1.2 sec", "Gemma Multimodal AI")

    st.markdown("---")

    # Zone & Category Filters
    f1, f2, f3 = st.columns([2, 2, 2])
    with f1:
        selected_zone = st.selectbox("Filter by GHMC Administrative Zone:", HYDERABAD_ZONES, index=0)
    with f2:
        selected_category = st.selectbox("Filter by Defect Category:", ["All Defect Categories"] + [v["label"] for v in ISSUE_CATEGORIES.values()], index=0)
    with f3:
        selected_urgency = st.selectbox("Filter by Urgency Level:", ["All Urgencies", "CRITICAL HAZARD (≥ 20)", "MODERATE PRIORITY (14-19)", "ROUTINE (< 14)"], index=0)

    # Filter incidents
    filtered_issues = []
    for issue in st.session_state.issues:
        sc = calculate_priority_score(issue["severity"], issue.get("repeat_count", 1), issue.get("accessibility_impact", 0))
        cat = ISSUE_CATEGORIES.get(issue.get("issue_type", "other"), ISSUE_CATEGORIES["other"])
        
        if selected_zone != "All GHMC Zones" and issue.get("zone") != selected_zone:
            continue
        if selected_category != "All Defect Categories" and cat["label"] != selected_category:
            continue
        if selected_urgency == "CRITICAL HAZARD (≥ 20)" and sc["score"] < 20:
            continue
        if selected_urgency == "MODERATE PRIORITY (14-19)" and not (14 <= sc["score"] < 20):
            continue
        if selected_urgency == "ROUTINE (< 14)" and sc["score"] >= 14:
            continue
            
        filtered_issues.append((issue, sc, cat))

    # Sort descending by priority score
    filtered_issues.sort(key=lambda x: x[1]["score"], reverse=True)

    # --------------------------------------------------------------------------
    # MAP WITH VISUAL INDICATIONS (PYDECK INTERACTIVE MAP)
    # --------------------------------------------------------------------------
    st.markdown("#### 🗺️ Hyderabad Civic Incident Map with Urgency Indications")
    st.caption("Interactive geospatial visualization. Colored markers indicate urgency; circle size indicates citizen complaint density.")

    # Prepare data for Pydeck
    map_data = []
    for issue, sc, cat in filtered_issues:
        # Radius expands with citizen report recurrence
        radius_val = max(180, min(issue.get("repeat_count", 1) * 90, 600))
        map_data.append({
            "name": issue.get("location_name", "Hyderabad Incident"),
            "zone": issue.get("zone", "GHMC Zone"),
            "ward": issue.get("ward", "GHMC Ward"),
            "category": cat["label"],
            "score": sc["score"],
            "band": sc["band"],
            "reports": issue.get("repeat_count", 1),
            "summary": issue.get("summary", ""),
            "lat": issue.get("lat", HYD_CENTER_LAT),
            "lon": issue.get("lon", HYD_CENTER_LON),
            "color": sc["pydeck_color"],
            "radius": radius_val
        })

    if map_data:
        df_map = pd.DataFrame(map_data)
        
        # Center view around Hyderabad incidents
        avg_lat = df_map["lat"].mean()
        avg_lon = df_map["lon"].mean()

        # Pydeck Scatterplot Layer
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map,
            get_position="[lon, lat]",
            get_color="color",
            get_radius="radius",
            pickable=True,
            opacity=0.85,
            stroked=True,
            filled=True,
            radius_min_pixels=8,
            radius_max_pixels=40,
            line_width_min_pixels=2,
            get_line_color=[255, 255, 255, 200]
        )

        view_state = pdk.ViewState(
            latitude=avg_lat,
            longitude=avg_lon,
            zoom=11.6,
            pitch=35
        )

        tooltip_config = {
            "html": "<b>{name}</b><br/>"
                    "<b>GHMC Zone:</b> {zone}<br/>"
                    "<b>Category:</b> {category}<br/>"
                    "<b>Urgency:</b> {band} (Score: {score})<br/>"
                    "<b>Citizen Reports:</b> {reports} complaints<br/>"
                    "<i>{summary}</i>",
            "style": {
                "backgroundColor": "#0f172a",
                "color": "#f8fafc",
                "fontSize": "13px",
                "borderRadius": "8px",
                "padding": "10px",
                "border": "1px solid #3b82f6"
            }
        }

        deck = pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            tooltip=tooltip_config,
            map_style="dark"
        )

        st.pydeck_chart(deck)
    else:
        st.warning("No incidents match the active filters to display on the map.")

    # Map Legend
    st.markdown(
        """
        <div style="background:#151c2c; border:1px solid #2a364f; border-radius:8px; padding:12px 18px; margin-top:8px; display:flex; gap:28px; flex-wrap:wrap; font-size:0.9em;">
            <span><span class="map-legend-dot-red"></span><b>Red:</b> Critical Hazard (Score ≥ 20) — Priority DRF / Road Dispatch</span>
            <span><span class="map-legend-dot-amber"></span><b>Amber:</b> Moderate Priority (Score 14–19) — Action within 48h</span>
            <span><span class="map-legend-dot-green"></span><b>Green:</b> Routine Maintenance (Score < 14) — Scheduled Sweeps</span>
            <span>⚪ <b>Circle Size:</b> Multiplies with Citizen Complaint Volume</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------------------------
    # PRIORITIZED WORK ORDER QUEUE
    # --------------------------------------------------------------------------
    st.markdown(f"#### 📋 Prioritized GHMC Work Order Queue ({len(filtered_issues)} Incidents)")

    card_idx = 0
    for issue, sc, cat in filtered_issues:
        card_idx += 1
        badge_emoji = "🚨" if sc["score"] >= 20 else ("⚠️" if sc["score"] >= 14 else "🟢")
        
        with st.expander(
            f"{badge_emoji} #{card_idx} · [{issue['id']}] {cat['icon']} {issue.get('issue_label', cat['label'])} | Location: {issue.get('location_name')} ({issue.get('zone')}) | Score: {sc['score']} pts",
            expanded=(card_idx == 1)
        ):
            c_d1, c_d2 = st.columns([3, 2])
            with c_d1:
                st.markdown(f"**Location:** 📍 {issue.get('location_name')} (`{issue.get('zone')}` · `{issue.get('ward')}`)")
                st.markdown(f"**Summary:** {issue.get('summary')}")
                st.markdown("**AI Visual Evidence Identified:**")
                for ev in issue.get("visible_evidence", []):
                    st.markdown(f"- 🔎 {ev}")
                
                st.markdown("**⚠️ What Requires Physical Field Verification (Uncertainty):**")
                st.info(issue.get("uncertainty", "Physical on-site inspection required."))
                
                st.markdown(f"**🛠️ Municipal Action:** `{issue.get('recommended_action')}`")

            with c_d2:
                st.markdown("#### Prioritization Breakdown")
                st.markdown(
                    f"""
                    - **Severity Hazard:** {sc['severity_val']}/5 ({sc['severity_pts']} pts)
                    - **Citizen Complaints:** {sc['repeat_val']} reports at this location ({sc['repeat_pts']} pts)
                    - **Accessibility / Transit Block:** {sc['accessibility_val']}/5 ({sc['accessibility_pts']} pts)
                    - **Computed Urgency Score:** **{sc['score']} points ({sc['band']})**
                    """
                )
                
                with st.expander("📐 View GHMC Scoring Heuristic"):
                    st.markdown(f"<div class='math-drawer'>{sc['explanation']}</div>", unsafe_allow_html=True)
                    st.caption("Transparent Rule: (Severity × 3) + min(Repeats - 1, 4) × 2 + (Accessibility × 2)")

                st.caption(f"Status: **{issue.get('status', 'Open')}** · Reported at: {issue.get('observed_at')}")

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Mark Resolved", key=f"res_{issue['id']}", use_container_width=True):
                        st.session_state.issues = [i for i in st.session_state.issues if i['id'] != issue['id']]
                        st.toast(f"Incident {issue['id']} marked as resolved by GHMC and closed.")
                        st.rerun()
                with col_btn2:
                    if st.button("📢 +1 Citizen Report", key=f"end_{issue['id']}", use_container_width=True):
                        issue['repeat_count'] = issue.get('repeat_count', 1) + 1
                        st.toast(f"Complaint count increased for {issue['id']}!")
                        st.rerun()

    if card_idx == 0:
        st.warning("No incidents found matching the selected filters.")

# ==============================================================================
# TAB 3: HYDERABAD HOTSPOT ANALYTICS & CLUSTERS
# ==============================================================================
with tab_hotspots:
    st.markdown("### 📍 Hyderabad Chronic Hotspot Surveillance")
    st.caption("CityPulse groups individual reports by physical Hyderabad locations, revealing chronic problem zones rather than isolated tickets.")

    h_col1, h_col2 = st.columns([1, 1], gap="medium")

    with h_col1:
        st.markdown("#### Recurring Location Hotspots (Ranked by Urgency)")
        for h in hotspots:
            st.markdown(
                f"""
                <div class="civic-card" style="padding:16px; margin-bottom:14px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.15em; font-weight:bold;">📍 {h['location_name']}</span>
                        <span style="color:#ef4444; font-weight:bold;">Peak Score: {h['highest_score']} pts</span>
                    </div>
                    <p style="color:#94a3b8; font-size:0.9em; margin:4px 0;">Zone: <b>{h['zone']}</b> | {h['ward']}</p>
                    <p>• <b>Citizen Complaints:</b> {h['total_citizen_reports']} reports clustered across {h['observation_count']} defects</p>
                    <p>• <b>Defect Types:</b> {', '.join([d.replace('_', ' ').title() for d in h['issue_types']])}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with h_col2:
        st.markdown("#### Zone-Wise Incident Distribution")
        zone_summary = {}
        for issue in st.session_state.issues:
            z = issue.get("zone", "Other")
            zone_summary[z] = zone_summary.get(z, 0) + issue.get("repeat_count", 1)

        df_zone = pd.DataFrame([
            {"GHMC Zone": k, "Total Citizen Complaints": v} 
            for k, v in zone_summary.items()
        ]).sort_values("Total Citizen Complaints", ascending=False)
        
        st.dataframe(df_zone, use_container_width=True, hide_index=True)
        st.bar_chart(df_zone.set_index("GHMC Zone"))

# ==============================================================================
# TAB 4: 45-SECOND PITCH & JUDGE DEMO
# ==============================================================================
with tab_pitch:
    st.markdown("### ⏱️ 45-Second Pitch Tailored for Hyderabad (GHMC)")
    st.caption("Deliver this sequence to demonstrate how CityPulse solves Hyderabad's distinct urban challenges:")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        #### 1. The Hyderabad Problem (0-10s)
        *"From Gachibowli waterlogging to Jubilee Hills potholes, GHMC receives thousands of fragmented citizen photos. But duplicate complaints clog the system without clear urgency ranking."*
        """)
    with p2:
        st.markdown("""
        #### 2. 1-Click Multimodal Triage (10-20s)
        *"With CityPulse, a citizen simply clicks a picture and picks their locality. Gemma multimodal AI diagnoses the visible hazard, extracts concrete evidence, and flags what cannot be seen from the photo."*
        """)
    with p3:
        st.markdown("""
        #### 3. Map Indications & Hotspots (20-30s)
        *"Instead of disconnected complaints, CityPulse clusters issues on an interactive Hyderabad map with red, amber, and green indications scaled by citizen report volume."*
        """)
    with p4:
        st.markdown("""
        #### 4. The Impact (30-45s)
        *"GHMC engineers and DRF teams immediately know which catch-pit or road crater poses the highest risk. CityPulse doesn't replace inspectors—it tells them where to look first."*
        """)

    st.markdown("---")
    st.info("💡 **Recommended Live Demo Flow:** Open **Tab 1**, select **📸 Use Live Camera** (or Sample #1 Gachibowli), click **🚀 Post Issue to GHMC**, then switch to **Tab 2** to show the live update on the Hyderabad map in under 30 seconds.")
