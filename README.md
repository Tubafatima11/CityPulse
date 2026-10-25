# CityPulse Hyderabad — GHMC Civic Connect 🏙️

> **Tagline:** Turn street footage into actionable infrastructure intelligence for Hyderabad.  
> **Target Civic Body:** Greater Hyderabad Municipal Corporation (GHMC) & Hyderabad Citizens.  
> **One-Line Pitch:** CityPulse turns everyday street photos from Hyderabad into a live, evidence-backed municipal maintenance queue—so GHMC and DRF teams can pinpoint recurring hotspots, see why they matter, and prioritize field repairs.

---

## 1. Hyderabad Problem & Civic Context
Hyderabad's rapid urban expansion and monsoon season create acute street infrastructure challenges:
- **Monsoon Waterlogging & Catch-Pit Choking:** Silt, debris, and plastic waste clog curb inlets in high-density corridors like Gachibowli, Madhapur, and Khairatabad, stalling traffic for hours.
- **Road Bitumen Deterioration:** Heavy monsoon rains and heavy RTC bus traffic cause deep potholes in busy transit lanes (e.g. Jubilee Hills Road 36, Kukatpally Y-Junction).
- **Pedestrian & Heritage Accessibility:** Uneven paving, broken storm manhole covers, and encroaching debris around busy corridors (e.g. Charminar Promenade, Secunderabad Station) pose severe pedestrian hazards.
- **Fragmented 311 Grievances:** Citizens post scattered photos on social media or dial GHMC hotlines, creating dozens of disconnected duplicate tickets for the same physical corner.

**CityPulse Hyderabad** solves this by:
1. Allowing any citizen to **snap a picture directly** using their phone or webcam, tag their Hyderabad locality, and post in under 15 seconds.
2. Running **Gemma Multimodal AI** to classify the hazard, extract concrete visual evidence, assess severity, and flag uncertainties.
3. Automatically clustering repeated reports into **physical hotspots** across GHMC administrative zones.
4. Providing GHMC officials with an **interactive map with color indications** and an explainable risk queue.

---

## 2. GHMC Administrative Zones & Coverage

- **Serilingampally (West Zone):** Hitec City, Gachibowli Bio-Diversity, Madhapur, Mindspace, Kondapur
- **Khairatabad (Central Zone):** Banjara Hills, Jubilee Hills, Somajiguda, Ameerpet
- **Charminar (South Zone):** Old City, Lad Bazaar, Falaknuma, Mehdipatnam
- **Secunderabad (North Zone):** Clock Tower, Begumpet, Marredpally, Paradise
- **Kukatpally (North-West Zone):** KPHB Colony, Y-Junction, Miyapur
- **LB Nagar (East Zone):** Dilsukhnagar, Kothapet, Saroornagar

---

## 3. Architecture & Data Flow

```text
Hyderabad street photo (Live Camera / Upload) + Locality
                         │
                         ▼
             Gemma Multimodal AI Triage
      (Extracts visible evidence, severity, uncertainty)
                         │
                         ▼
        GHMC Structured Incident Observation
                         │
                         ▼
      Geographic Hotspot Clustering (GHMC Zones)
                         │
                         ▼
     Deterministic Priority Scoring Heuristic
   Score = (Severity × 3) + min(Repeats - 1, 4) × 2 + (Accessibility × 2)
                         │
                         ▼
        GHMC Official Dashboard & Live Map
    (Red / Amber / Green visual indications + Work Orders)
```

---

## 4. Map Indications & Transparent Prioritization

### Interactive Pydeck Map Visual Indications:
- 🔴 **Red Pins (Critical Hazard, Score ≥ 20):** High hazard to commuter safety or transit flow. Escalated for immediate GHMC Disaster Response Force (DRF) or road repair squad dispatch.
- 🟠 **Amber Pins (Moderate Priority, Score 14–19):** Urgent defect; requires action within 24–48 hours to prevent deterioration.
- 🟢 **Green Pins (Routine Maintenance, Score < 14):** Logged for standard municipal sweeps and scheduled upkeep.
- ⚪ **Pin Size:** Expands dynamically based on citizen complaint volume at that specific spot.

### Priority Formula:
$$\text{Priority Score} = (\text{Severity} \times 3) + \min(\text{Repeats} - 1, 4) \times 2 + (\text{Accessibility} \times 2)$$

---

## 5. Quickstart: Running CityPulse Hyderabad

### Local Server Launch
```powershell
& "C:\Users\Moiz\AppData\Local\Programs\Python\Python311\Scripts\streamlit.exe" run "C:\Users\Moiz\.gemini\antigravity\scratch\citypulse\app.py"
```

Open your browser at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 6. 45-Second Pitch Script for GHMC

| Time | Tab | Spoken Script |
|------|-----|---------------|
| **0–10s** | Citizen Corner | *"From Gachibowli waterlogging to Jubilee Hills potholes, GHMC receives thousands of fragmented citizen complaints with no consistent way to prioritize."* |
| **10–20s** | Citizen Corner | *"With CityPulse, a resident snaps a photo and picks their locality. Gemma multimodal AI diagnoses the hazard, extracts concrete evidence, and assigns urgency in under 2 seconds."* |
| **20–30s** | GHMC Official Dashboard | *"On the GHMC dashboard, issues appear live on an interactive Hyderabad map with red, amber, and green indications scaled by complaint volume."* |
| **30–45s** | Official Dashboard | *"GHMC engineers and DRF teams immediately see which drain or crater needs emergency dispatch. CityPulse doesn't replace inspectors—it tells them where to look first."* |
