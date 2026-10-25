"""
CityPulse — Gemma / Multimodal Triage Engine
Extracts structured infrastructure observations from street imagery and resident descriptions.
Supports live API inference with zero mandatory external SDKs (uses standard urllib),
with graceful, transparent fallback to offline demo triage.
"""

import os
import json
import base64
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple

SYSTEM_PROMPT = """You are CityPulse, an assistant that triages visible street-infrastructure issues.

Analyze the supplied image and optional resident description. Return one valid JSON object only, using these fields:
- issue_type: one of pothole, blocked_drain, overflowing_rubbish, broken_footpath, accessibility_barrier, other, unclear
- summary: one short sentence
- visible_evidence: array of concrete observations visible in the image
- severity: integer from 1 to 5, or null if evidence is insufficient
- accessibility_impact: integer from 0 to 5, or null if uncertain
- uncertainty: what cannot be established from the evidence
- recommended_action: a reasonable inspection or verification step

Rules:
- Do not invent location, coordinates, ownership, dimensions, costs, or hidden conditions.
- Distinguish direct visual evidence from inference.
- Do not claim that a drain is blocked unless the image supports that conclusion; use "possible obstruction" when uncertain.
- Do not infer that a defect is getting worse from a single image.
- This is triage support, not a safety certification.
- Return JSON only. No markdown formatting outside of JSON.
"""

# Realistic offline triage presets for smooth 30-minute hackathon demo without network dependencies
OFFLINE_PRESETS = {
    "blocked_drain": {
        "issue_type": "blocked_drain",
        "summary": "Storm drain opening is obstructed by leaf litter, gravel, and organic runoff.",
        "visible_evidence": [
            "Dense deposit of leaves and urban silt over the curb inlet opening",
            "Standing surface water pooling along the asphalt gutter line",
            "Curb drop inlet grate partially submerged under debris"
        ],
        "severity": 4,
        "accessibility_impact": 1,
        "uncertainty": "Interior basin blockage, pipe siltation level, and flow capacity under heavy precipitation cannot be verified without physical drain inspection.",
        "recommended_action": "Schedule vacuum truck clean-out and verify subsurface drain line clearance."
    },
    "broken_footpath": {
        "issue_type": "broken_footpath",
        "summary": "Concrete sidewalk slab shows severe vertical displacement and fracture.",
        "visible_evidence": [
            "Continuous shear crack across pedestrian pathway with ~2.5 inch vertical step fault",
            "Displaced flagstone creating a significant trip ledge in direct walking line",
            "Usable ADA clearance width reduced below 32 inches"
        ],
        "severity": 3,
        "accessibility_impact": 5,
        "uncertainty": "Sub-slab tree root progression rate, soil void size, and subterranean utility conflict cannot be confirmed from surface view.",
        "recommended_action": "Apply temporary high-visibility warning paint and cold-mix ramp; schedule permanent concrete slab grinding or repour."
    },
    "pothole": {
        "issue_type": "pothole",
        "summary": "Pothole cavity with broken asphalt edges located in vehicular travel lane.",
        "visible_evidence": [
            "Irregular surface void roughly 18 inches across with exposed base gravel",
            "Sharp crumbling asphalt perimeter edges prone to further vehicle tire impact",
            "Asphalt debris scattered in adjacent bike lane"
        ],
        "severity": 4,
        "accessibility_impact": 1,
        "uncertainty": "Cavity depth under standing sediment, water intrusion into subbase, and load-bearing subgrade damage cannot be measured from photo.",
        "recommended_action": "Mark with traffic cone; dispatch asphalt patching crew for hot/cold mix compaction within 48 hours."
    },
    "overflowing_rubbish": {
        "issue_type": "overflowing_rubbish",
        "summary": "Public waste receptacle overflowing with loose refuse encroaching sidewalk.",
        "visible_evidence": [
            "Commercial cartons and beverage containers stacked 18+ inches above receptacle rim",
            "Litter spillage extending across 3 feet of adjacent pedestrian curb zone",
            "Bagged household garbage placed alongside bin foundation"
        ],
        "severity": 2,
        "accessibility_impact": 2,
        "uncertainty": "Hazardous materials, sharp glass inside unsealed sacks, or biological waste presence cannot be safely verified visually.",
        "recommended_action": "Route priority sanitation sweep and evaluate bin capacity or collection frequency for this location."
    }
}

def clean_json_text(text: str) -> str:
    """Strip markdown code fence blocks if returned by model."""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

def validate_observation_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure all required fields exist and conform to CityPulse standards."""
    valid_types = {
        "pothole", "blocked_drain", "overflowing_rubbish", 
        "broken_footpath", "accessibility_barrier", "other", "unclear"
    }
    
    raw_type = str(data.get("issue_type", "other")).lower().strip().replace(" ", "_").replace("-", "_")
    issue_type = raw_type if raw_type in valid_types else "other"
    
    # Severity 1-5
    try:
        sev = int(data.get("severity"))
        sev = max(1, min(sev, 5))
    except (ValueError, TypeError):
        sev = 3
        
    # Accessibility impact 0-5
    try:
        acc = int(data.get("accessibility_impact"))
        acc = max(0, min(acc, 5))
    except (ValueError, TypeError):
        acc = 1

    evidence = data.get("visible_evidence", [])
    if isinstance(evidence, str):
        evidence = [evidence]
    elif not isinstance(evidence, list) or len(evidence) == 0:
        evidence = ["Visible defect present in captured frame"]

    return {
        "issue_type": issue_type,
        "summary": str(data.get("summary", "Infrastructure condition observed.")),
        "visible_evidence": [str(e) for e in evidence],
        "severity": sev,
        "accessibility_impact": acc,
        "uncertainty": str(data.get("uncertainty", "Full subsurface condition and hidden damage cannot be determined from photograph alone.")),
        "recommended_action": str(data.get("recommended_action", "Conduct on-site visual and tactile physical inspection."))
    }

def call_gemini_multimodal_api(
    image_bytes: bytes,
    mime_type: str,
    description: Optional[str] = None,
    api_key: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Calls Google Gemini multimodal endpoint using standard library urllib.
    Returns (parsed_json, error_message).
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return None, "No GEMINI_API_KEY or GOOGLE_API_KEY found."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    user_prompt = "Examine this street infrastructure photograph."
    if description and description.strip():
        user_prompt += f"\nResident description: {description.strip()}"
        
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + user_prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type or "image/jpeg",
                            "data": b64_image
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp_body = resp.read().decode("utf-8")
            resp_json = json.loads(resp_body)
            candidates = resp_json.get("candidates", [])
            if not candidates:
                return None, "Empty response candidates from model."
            
            raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            cleaned = clean_json_text(raw_text)
            parsed = json.loads(cleaned)
            return validate_observation_schema(parsed), None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return None, f"HTTP {e.code}: {err_body[:200]}"
    except Exception as e:
        return None, str(e)

def analyze_observation(
    image_bytes: Optional[bytes] = None,
    mime_type: str = "image/jpeg",
    description: Optional[str] = None,
    preset_key: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point for CityPulse triage.
    Tries live API if configured, otherwise falls back smoothly to offline intelligence.
    """
    # 1. Attempt live API if key is provided and image bytes exist
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key and image_bytes:
        parsed, err = call_gemini_multimodal_api(image_bytes, mime_type, description, key)
        if parsed:
            return {
                "source": "Live Multimodal Model (Gemini / Gemma Vision API)",
                "live_api_used": True,
                "data": parsed,
                "note": "AI-assisted triage output. Human inspection required before dispatch."
            }
        else:
            # Live call failed, record error and proceed to graceful fallback
            fallback_reason = f"Live API call unfulfilled ({err}). Fell back to offline triage preset."
    else:
        fallback_reason = "Operating in offline demo mode (no API key provided). Using deterministic heuristic preset."

    # 2. Offline / Preset Fallback
    # Identify best matching preset based on description or preset_key
    selected_preset = preset_key or "broken_footpath"
    if description:
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["drain", "water", "flood", "sewer", "gutter", "runoff", "clog"]):
            selected_preset = "blocked_drain"
        elif any(w in desc_lower for w in ["pothole", "asphalt", "crater", "road", "cavity", "tire"]):
            selected_preset = "pothole"
        elif any(w in desc_lower for w in ["trash", "garbage", "rubbish", "waste", "bin", "litter"]):
            selected_preset = "overflowing_rubbish"
        elif any(w in desc_lower for w in ["sidewalk", "footpath", "paving", "curb", "trip", "pedestrian", "walkway"]):
            selected_preset = "broken_footpath"

    data = OFFLINE_PRESETS.get(selected_preset, OFFLINE_PRESETS["broken_footpath"]).copy()
    
    # If user provided a custom description, weave it into summary
    if description and description.strip():
        data["summary"] = f"{data['summary']} [Citizen note: \"{description.strip()[:60]}...\"]"
        
    return {
        "source": "Deterministic Demo Preset (Offline Fallback)",
        "live_api_used": False,
        "fallback_reason": fallback_reason,
        "data": validate_observation_schema(data),
        "note": "Demo heuristic fallback. Connect Gemma / Gemini API for live vision inference."
    }
