"""
CityPulse — Sample Dataset & Business Logic
Contains preloaded demo records, recurrence grouping, and transparent priority scoring.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional

# Synthetic base coordinates for demo map visualization (Civic District)
BASE_LAT = 37.7749
BASE_LON = -122.4194

SAMPLE_ISSUES: List[Dict[str, Any]] = [
    {
        "id": "CP-101",
        "location_id": "BLOCK-A",
        "location_name": "7th & Market St (Drain Inflow)",
        "lat": BASE_LAT + 0.0035,
        "lon": BASE_LON - 0.0020,
        "issue_type": "blocked_drain",
        "issue_label": "Severe Storm Drain Obstruction",
        "summary": "Heavy organic debris and plastic silt obstruction covers ~80% of drain grating.",
        "severity": 4,
        "accessibility_impact": 1,
        "repeat_count": 4,
        "visible_evidence": [
            "Dense mulch, tree clippings, and plastic bottles clogging iron grate",
            "Visible standing runoff pooling 4 inches past curb onto bike lane"
        ],
        "uncertainty": "Subsurface pipe blockage and catch-basin fill level cannot be verified from surface imagery.",
        "recommended_action": "High-priority vac-truck crew dispatch to clear surface grate and inspect basin depth.",
        "observed_at": "2026-10-25 08:30",
        "status": "Flagged for Inspection",
        "verified_location": True
    },
    {
        "id": "CP-102",
        "location_id": "BLOCK-B",
        "location_name": "Elmwood Pedestrian Walkway",
        "lat": BASE_LAT - 0.0018,
        "lon": BASE_LON + 0.0042,
        "issue_type": "broken_footpath",
        "issue_label": "Upheaved Concrete & Accessibility Hazard",
        "summary": "Tree root upheaval has created a 2.5-inch vertical lip across primary sidewalk corridor.",
        "severity": 3,
        "accessibility_impact": 5,
        "repeat_count": 3,
        "visible_evidence": [
            "Continuous diagonal fracture with >2 inch slab displacement",
            "Clear walkway reduced to under 24 inches width, blocking wheelchair / stroller passage"
        ],
        "uncertainty": "Active tree root expansion depth and underlying utility line proximity require ground scanner.",
        "recommended_action": "Deploy temporary asphalt transition ramp; schedule pavement grinding or slab repour.",
        "observed_at": "2026-10-24 17:15",
        "status": "Flagged for Inspection",
        "verified_location": True
    },
    {
        "id": "CP-103",
        "location_id": "BLOCK-C",
        "location_name": "4th Ave & Transit Hub Crossing",
        "lat": BASE_LAT + 0.0012,
        "lon": BASE_LON + 0.0015,
        "issue_type": "pothole",
        "issue_label": "Deep Road Surface Depression",
        "summary": "Edge pothole with exposed aggregate in high-traffic bus deceleration zone.",
        "severity": 4,
        "accessibility_impact": 1,
        "repeat_count": 2,
        "visible_evidence": [
            "Sharp perimeter edge with loose gravel dispersal across 1m radius",
            "Located directly in cyclist and curbside transit wheel path"
        ],
        "uncertainty": "Subbase compaction integrity and cavity depth below visible gravel line cannot be measured.",
        "recommended_action": "Mark with high-visibility reflector cone; schedule cold-patch asphalt crew within 48h.",
        "observed_at": "2026-10-25 09:10",
        "status": "Triage Queued",
        "verified_location": True
    },
    {
        "id": "CP-104",
        "location_id": "BLOCK-D",
        "location_name": "Pine St Commercial Alleyway",
        "lat": BASE_LAT - 0.0040,
        "lon": BASE_LON - 0.0035,
        "issue_type": "overflowing_rubbish",
        "issue_label": "Overflowing Public Receptacle & Alley Spillage",
        "summary": "Municipal waste bin overwhelmed with commercial cardboard and bags encroaching walkway.",
        "severity": 2,
        "accessibility_impact": 2,
        "repeat_count": 1,
        "visible_evidence": [
            "Cardboard and plastic bags piled 1.5 ft above bin rim",
            "Spillage restricting side alley pedestrian clearance"
        ],
        "uncertainty": "Hazardous or chemical materials inside sealed bags cannot be determined visually.",
        "recommended_action": "Route extra sanitation sweep; evaluate bin capacity upgrade with local merchant association.",
        "observed_at": "2026-10-25 10:45",
        "status": "Low Urgency",
        "verified_location": True
    },
    {
        "id": "CP-105",
        "location_id": "BLOCK-A",
        "location_name": "7th & Market St (Crosswalk)",
        "lat": BASE_LAT + 0.0038,
        "lon": BASE_LON - 0.0019,
        "issue_type": "broken_footpath",
        "issue_label": "Missing Tactile Paving on Curb Ramp",
        "summary": "Worn or missing truncated domes on ADA pedestrian curb ramp entrance.",
        "severity": 3,
        "accessibility_impact": 4,
        "repeat_count": 1,
        "visible_evidence": [
            "Eroded tactile yellow warning tile with multiple missing studs",
            "Located at busy signalized intersection crossing"
        ],
        "uncertainty": "Slipperiness rating and underlying adhesive condition under wet weather require tactile check.",
        "recommended_action": "Replace tactile warning surface tile per ADA accessibility standards.",
        "observed_at": "2026-10-25 11:20",
        "status": "Triage Queued",
        "verified_location": True
    }
]

ISSUE_CATEGORIES = {
    "blocked_drain": {"label": "Blocked Drain", "icon": "🌊", "color": "#1E88E5"},
    "broken_footpath": {"label": "Broken Footpath / Sidewalk", "icon": "🚶", "color": "#FB8C00"},
    "pothole": {"label": "Pothole / Road Defect", "icon": "🕳️", "color": "#E53935"},
    "overflowing_rubbish": {"label": "Overflowing Rubbish", "icon": "🗑️", "color": "#8E24AA"},
    "accessibility_barrier": {"label": "Accessibility Barrier", "icon": "♿", "color": "#00ACC1"},
    "other": {"label": "Other Infrastructure", "icon": "📍", "color": "#757575"}
}

def calculate_priority_score(severity: int, repeat_count: int, accessibility_impact: int) -> Dict[str, Any]:
    """
    Transparent municipal priority scoring heuristic:
    Score = (Severity * 3) + (min(Repeats - 1, 4) * 2) + (Accessibility * 2)
    Max theoretical score = (5 * 3) + (4 * 2) + (5 * 2) = 15 + 8 + 10 = 33
    """
    sev = max(1, min(int(severity or 1), 5))
    rep = max(1, int(repeat_count or 1))
    acc = max(0, min(int(accessibility_impact or 0), 5))

    severity_points = sev * 3
    repeat_bonus = min(rep - 1, 4) * 2
    accessibility_points = acc * 2
    total = severity_points + repeat_bonus + accessibility_points

    if total >= 20:
        band = "HIGH URGENCY"
        badge_color = "#D32F2F"
    elif total >= 14:
        band = "MEDIUM PRIORITY"
        badge_color = "#F57C00"
    else:
        band = "ROUTINE REVIEW"
        badge_color = "#388E3C"

    return {
        "score": total,
        "band": band,
        "badge_color": badge_color,
        "severity_val": sev,
        "severity_pts": severity_points,
        "repeat_val": rep,
        "repeat_pts": repeat_bonus,
        "accessibility_val": acc,
        "accessibility_pts": accessibility_points,
        "explanation": f"{sev}×3 ({severity_points}pts) + min({rep}-1, 4)×2 ({repeat_bonus}pts) + {acc}×2 ({accessibility_points}pts)"
    }

def group_observations_by_hotspot(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Groups observations by location_id to highlight multi-issue recurring hotspots.
    """
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for issue in issues:
        loc = issue.get("location_id", "UNKNOWN")
        groups.setdefault(loc, []).append(issue)

    hotspots = []
    for loc_id, items in groups.items():
        total_reports = sum(item.get("repeat_count", 1) for item in items)
        max_score = max(calculate_priority_score(item["severity"], item.get("repeat_count", 1), item.get("accessibility_impact", 0))["score"] for item in items)
        issue_types = list({item.get("issue_type", "other") for item in items})
        loc_name = items[0].get("location_name", loc_id)
        hotspots.append({
            "location_id": loc_id,
            "location_name": loc_name,
            "observation_count": len(items),
            "total_citizen_reports": total_reports,
            "highest_score": max_score,
            "issue_types": issue_types,
            "items": items,
            "lat": items[0].get("lat", BASE_LAT),
            "lon": items[0].get("lon", BASE_LON)
        })

    hotspots.sort(key=lambda h: h["highest_score"], reverse=True)
    return hotspots
