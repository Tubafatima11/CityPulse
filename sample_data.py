"""
CityPulse Hyderabad (GHMC Edition) — Dataset & Civic Logic
Tailored for the Greater Hyderabad Municipal Corporation (GHMC) and citizens of Hyderabad.
"""

from typing import Dict, List, Any, Tuple

# Center coordinates for Hyderabad (Telangana, India)
HYD_CENTER_LAT = 17.3850
HYD_CENTER_LON = 78.4867

HYDERABAD_ZONES = [
    "All GHMC Zones",
    "Serilingampally (West Zone)",
    "Khairatabad (Central Zone)",
    "Charminar (South Zone)",
    "Secunderabad (North Zone)",
    "Kukatpally (North-West Zone)",
    "LB Nagar (East Zone)"
]

# Popular Hyderabad Localities with authentic Lat/Lon coordinates and GHMC Zone
HYDERABAD_LOCALITIES: Dict[str, Tuple[float, float, str]] = {
    "Gachibowli Bio-Diversity Junction (Ikea Underpass)": (17.4401, 78.3489, "Serilingampally (West Zone)"),
    "Hitec City Cyber Towers (Mindspace Junction)": (17.4504, 78.3808, "Serilingampally (West Zone)"),
    "Madhapur Main Road (Near Inorbit Mall)": (17.4334, 78.3866, "Serilingampally (West Zone)"),
    "Road No. 36, Jubilee Hills (Metro Pillar 1650)": (17.4319, 78.4073, "Khairatabad (Central Zone)"),
    "Road No. 12, Banjara Hills (Near MLA Colony)": (17.4156, 78.4350, "Khairatabad (Central Zone)"),
    "Charminar Pedestrian Promenade (Lad Bazaar)": (17.3616, 78.4747, "Charminar (South Zone)"),
    "Secunderabad Clock Tower Circle": (17.4415, 78.5002, "Secunderabad (North Zone)"),
    "Kukatpally Y-Junction (Metro Station Service Road)": (17.4938, 78.3995, "Kukatpally (North-West Zone)"),
    "Dilsukhnagar Main Road (Near Bus Station)": (17.3688, 78.5247, "LB Nagar (East Zone)"),
    "Ameerpet Metro Interchange (SR Nagar Crossroad)": (17.4375, 78.4482, "Khairatabad (Central Zone)"),
    "Mehdipatnam Rythu Bazar (PVNR Expressway Pillar 45)": (17.3916, 78.4411, "Charminar (South Zone)"),
    "Other / Custom Hyderabad Location": (17.4100, 78.4500, "Khairatabad (Central Zone)")
}

SAMPLE_ISSUES: List[Dict[str, Any]] = [
    {
        "id": "GHMC-401",
        "zone": "Serilingampally (West Zone)",
        "location_name": "Gachibowli Bio-Diversity Junction (Ikea Underpass)",
        "ward": "Ward 105 - Gachibowli",
        "lat": 17.4401,
        "lon": 78.3489,
        "issue_type": "blocked_drain",
        "issue_label": "Severe Stormwater Catch-Pit Blockage",
        "summary": "Monsoon stormwater inlet grate heavily choked by silt, thermocol, and plastic waste causing 5-inch standing pool into IT corridor.",
        "severity": 4,
        "accessibility_impact": 4,
        "repeat_count": 5,
        "visible_evidence": [
            "Dense mulch, urban silt, and plastic bottles blocking >85% of iron curb inlet",
            "Waterlogging extending 12 feet into outer vehicular and two-wheeler lane",
            "Adjacent pedestrian footpath submerged under muddy runoff"
        ],
        "uncertainty": "Subsurface RCC drain pipe blockage and downstream culvert flow capacity cannot be verified without de-silting shaft inspection.",
        "recommended_action": "Dispatch GHMC Disaster Response Force (DRF) Super Sucker vac-truck unit; clear silt trap immediately.",
        "observed_at": "2026-10-25 09:15",
        "status": "Escalated to DRF",
        "verified_location": True
    },
    {
        "id": "GHMC-402",
        "zone": "Khairatabad (Central Zone)",
        "location_name": "Road No. 36, Jubilee Hills (Metro Pillar 1650)",
        "ward": "Ward 95 - Jubilee Hills",
        "lat": 17.4319,
        "lon": 78.4073,
        "issue_type": "pothole",
        "issue_label": "Deep Road Surface Crater & Bitumen Shear",
        "summary": "Large asphalt cavity with sharp jagged edges situated directly in the middle transit lane under metro line.",
        "severity": 4,
        "accessibility_impact": 2,
        "repeat_count": 4,
        "visible_evidence": [
            "Asphalt crater ~2 feet in diameter with exposed loose subbase aggregate",
            "Multiple motorists and two-wheeler riders swerving abruptly to avoid rim damage",
            "Dispersed gravel scattered across 6-foot radius"
        ],
        "uncertainty": "Water penetration into lower water-bound macadam (WBM) layer and underlying soil stability require moisture gauge.",
        "recommended_action": "Erect reflective safety cones immediately; schedule hot-mix bitumen compaction patch within 24 hours.",
        "observed_at": "2026-10-25 10:30",
        "status": "Work Order Issued",
        "verified_location": True
    },
    {
        "id": "GHMC-403",
        "zone": "Charminar (South Zone)",
        "location_name": "Charminar Pedestrian Promenade (Lad Bazaar)",
        "ward": "Ward 50 - Charminar",
        "lat": 17.3616,
        "lon": 78.4747,
        "issue_type": "broken_footpath",
        "issue_label": "Heritage Paving Slab Upheaval & Trip Ledge",
        "summary": "Granite paving slab displacement of ~2.5 inches across primary tourist pedestrian walking corridor.",
        "severity": 3,
        "accessibility_impact": 5,
        "repeat_count": 3,
        "visible_evidence": [
            "Raised granite slab creating an abrupt vertical trip hazard in crowded market precinct",
            "Passage width for wheelchairs, prams, and senior citizens severely restricted",
            "Cracked interlocking border tile with missing grout"
        ],
        "uncertainty": "Underground cable duct or water pipeline leak below the slab cannot be confirmed from surface view.",
        "recommended_action": "Level flagstone base with compacted stone dust; re-grout perimeter paving to restore barrier-free walkway.",
        "observed_at": "2026-10-25 08:45",
        "status": "Flagged for Inspection",
        "verified_location": True
    },
    {
        "id": "GHMC-404",
        "zone": "Kukatpally (North-West Zone)",
        "location_name": "Kukatpally Y-Junction (Metro Station Service Road)",
        "ward": "Ward 120 - Kukatpally",
        "lat": 17.4938,
        "lon": 78.3995,
        "issue_type": "overflowing_rubbish",
        "issue_label": "Commercial Garbage Dumper Spill & Transit Encroachment",
        "summary": "GHMC community dumper bin overflowing with commercial cardboard and plastic packing encroaching onto auto-rickshaw lane.",
        "severity": 2,
        "accessibility_impact": 3,
        "repeat_count": 2,
        "visible_evidence": [
            "Refuse stacked 2 feet over dumper bin walls",
            "Spillage covering 15 feet of service road shoulder, forcing pedestrians into busy traffic",
            "Stray cattle foraging around open waste"
        ],
        "uncertainty": "Hazardous industrial scrap or contaminated biological waste within bags cannot be determined visually.",
        "recommended_action": "Route priority GHMC compactor truck sweep; install secondary bin or increase collection rounds.",
        "observed_at": "2026-10-25 11:10",
        "status": "Assigned to Sanitation Wing",
        "verified_location": True
    },
    {
        "id": "GHMC-405",
        "zone": "Secunderabad (North Zone)",
        "location_name": "Secunderabad Clock Tower Circle",
        "ward": "Ward 147 - Secunderabad",
        "lat": 17.4415,
        "lon": 78.5002,
        "issue_type": "broken_footpath",
        "issue_label": "Broken Storm Sewer Chamber Cover",
        "summary": "Severely fractured manhole slab on pedestrian sidewalk near heritage clock tower bus shelter.",
        "severity": 5,
        "accessibility_impact": 4,
        "repeat_count": 4,
        "visible_evidence": [
            "Fractured concrete lid with exposed rusted rebar mesh",
            "Open cavity into 6-foot drain shaft directly in walking path of transit commuters",
            "Temporary wooden plank placed by locals as crude warning"
        ],
        "uncertainty": "Structural integrity of concrete ring collar and brick masonry wall inside the chamber.",
        "recommended_action": "EMERGENCY: Barricade perimeter immediately; replace with heavy-duty ductile iron SFRC manhole cover today.",
        "observed_at": "2026-10-25 07:40",
        "status": "Emergency Dispatch",
        "verified_location": True
    }
]

ISSUE_CATEGORIES = {
    "blocked_drain": {"label": "Blocked Drain / Nala Overflow", "icon": "🌊", "color": "#1E88E5"},
    "broken_footpath": {"label": "Broken Footpath / Manhole Defect", "icon": "🚶", "color": "#FB8C00"},
    "pothole": {"label": "Road Pothole / Bitumen Damage", "icon": "🕳️", "color": "#E53935"},
    "overflowing_rubbish": {"label": "Overflowing Garbage / Dumper", "icon": "🗑️", "color": "#8E24AA"},
    "accessibility_barrier": {"label": "Accessibility / ADA Barrier", "icon": "♿", "color": "#00ACC1"},
    "other": {"label": "Other Civic Infrastructure", "icon": "📍", "color": "#757575"}
}

def calculate_priority_score(severity: int, repeat_count: int, accessibility_impact: int) -> Dict[str, Any]:
    """
    Transparent municipal priority scoring heuristic:
    Score = (Severity * 3) + (min(Repeats - 1, 4) * 2) + (Accessibility * 2)
    Max theoretical score = 33
    """
    sev = max(1, min(int(severity or 1), 5))
    rep = max(1, int(repeat_count or 1))
    acc = max(0, min(int(accessibility_impact or 0), 5))

    severity_points = sev * 3
    repeat_bonus = min(rep - 1, 4) * 2
    accessibility_points = acc * 2
    total = severity_points + repeat_bonus + accessibility_points

    if total >= 20:
        band = "CRITICAL HAZARD (HIGH URGENCY)"
        badge_color = "#D32F2F"
        pydeck_color = [239, 68, 68, 220] # Red
    elif total >= 14:
        band = "MODERATE PRIORITY"
        badge_color = "#F57C00"
        pydeck_color = [245, 158, 11, 200] # Amber
    else:
        band = "ROUTINE MAINTENANCE"
        badge_color = "#388E3C"
        pydeck_color = [16, 185, 129, 180] # Green

    return {
        "score": total,
        "band": band,
        "badge_color": badge_color,
        "pydeck_color": pydeck_color,
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
    Groups observations by location name and GHMC zone to highlight multi-issue recurring hotspots.
    """
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for issue in issues:
        loc = issue.get("location_name", "Unknown Location")
        groups.setdefault(loc, []).append(issue)

    hotspots = []
    for loc_name, items in groups.items():
        total_reports = sum(item.get("repeat_count", 1) for item in items)
        max_score = max(calculate_priority_score(item["severity"], item.get("repeat_count", 1), item.get("accessibility_impact", 0))["score"] for item in items)
        issue_types = list({item.get("issue_type", "other") for item in items})
        zone = items[0].get("zone", "GHMC Zone")
        ward = items[0].get("ward", "GHMC Ward")
        
        # Color based on peak score
        if max_score >= 20:
            color = [239, 68, 68, 220]
            urgency_label = "CRITICAL HOTSPOT"
        elif max_score >= 14:
            color = [245, 158, 11, 200]
            urgency_label = "MODERATE HOTSPOT"
        else:
            color = [16, 185, 129, 180]
            urgency_label = "ROUTINE"

        hotspots.append({
            "location_name": loc_name,
            "zone": zone,
            "ward": ward,
            "observation_count": len(items),
            "total_citizen_reports": total_reports,
            "highest_score": max_score,
            "urgency_label": urgency_label,
            "issue_types": issue_types,
            "items": items,
            "lat": items[0].get("lat", HYD_CENTER_LAT),
            "lon": items[0].get("lon", HYD_CENTER_LON),
            "pydeck_color": color,
            "radius": max(120, min(total_reports * 60, 450))
        })

    hotspots.sort(key=lambda h: h["highest_score"], reverse=True)
    return hotspots
