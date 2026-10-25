# CityPulse — 30-Minute Hackathon Prototype 🏙️

> **Tagline:** Turn street footage into actionable infrastructure intelligence.  
> **One-Line Pitch:** CityPulse turns everyday street imagery into a live, evidence-backed maintenance queue—so city teams can see recurring problems, understand why they matter, and decide what to inspect first.

---

## 1. Problem & Context
Municipal public works departments receive thousands of fragmented citizen complaints each month detailing broken footpaths, clogged storm drains, potholes, and overflowing refuse. These reports:
1. Arrive in disparate descriptions without visual standardization.
2. Fragment identical physical locations into separate disconnected tickets.
3. Lack transparent prioritization, forcing city teams to guess which defect poses immediate risk.

**CityPulse** bridges this gap:
- **Multimodal AI (Gemma / Gemini Vision):** Converts street photos and resident notes into structured visible evidence, severity ratings, and uncertainty flags without hallucinating unseen subbase damage.
- **Recurrence Hotspot Clustering:** Automatically correlates reports by physical location identifiers.
- **Explainable Priority Heuristic:** Computes an inspect-first priority ranking using transparent civic weighting.

> ⚠️ **Safety & Scope Notice:** CityPulse provides AI-assisted triage support, not structural engineering certification or predictive deterioration modeling. A human inspector must verify all defects before dispatch. All demonstration records are synthetic.

---

## 2. Architecture & Data Flow

```text
Street photo / sample video frame / resident note
                         │
                         ▼
             Gemma Multimodal Triage
      (Extracts visible evidence, severity, uncertainty)
                         │
                         ▼
             Structured JSON Observation
                         │
                         ▼
       Location Clustering & Recurrence Grouping
                         │
                         ▼
     Deterministic Priority Scoring Heuristic
   Score = (Severity × 3) + min(Repeats - 1, 4) × 2 + (Accessibility × 2)
                         │
                         ▼
          CityPulse Interactive Dashboard
      (Priority Queue, Hotspot Map, Inspection Actions)
```

### Why Separate Model Inference & Scoring?
- **Multimodal Model (Gemma / Gemini):** Interprets unstructured visual reality, identifies defects, surfaces concrete visible evidence, and explicitly flags what *cannot* be seen (e.g. pipe depth, subbase voids).
- **Deterministic Code (Python):** Handles exact counting, duplicate deduplication, hotspot clustering, and transparent formula scoring. Eliminates black-box scoring.

---

## 3. Transparent Priority Scoring Heuristic

$$\text{Priority Score} = (\text{Severity} \times 3) + \min(\text{Repeats} - 1, 4) \times 2 + (\text{Accessibility Impact} \times 2)$$

- **Severity (1–5, weighted $\times 3$):** Direct physical hazard or structural degradation observed.
- **Recurrence ($\min(\text{Repeats}-1, 4) \times 2$):** Citizen complaint frequency at this specific location (caps at 4 repeats / 8 bonus points to avoid spam dominance).
- **Accessibility Impact (0–5, weighted $\times 2$):** Obstruction to wheelchairs, strollers, cane-users, or transit crossings.

### Example:
- Severity: 4 $\rightarrow$ 12 pts
- Repeated observations: 3 $\rightarrow$ 4 pts
- Accessibility impact: 2 $\rightarrow$ 4 pts
- **Total: 20 pts (HIGH URGENCY)**

---

## 4. Quickstart: Running CityPulse

### Prerequisites
- Python 3.10+
- Streamlit & Pillow (installed automatically via requirements)

### Installation & Launch
```bash
cd "C:\Users\Moiz\.gemini\antigravity\scratch\citypulse"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Optional Live Gemma / Gemini API
CityPulse includes high-fidelity deterministic offline presets so **the demo works 100% offline with zero setup**. If you wish to enable live multimodal inference with your own Google Gemini or Gemma API key:
- Pass your key in the Streamlit sidebar input, or:
- Set environment variable: `set GEMINI_API_KEY=your_api_key_here`

---

## 5. 45-Second Judge Demo Sequence

| Time | Action | What to Say |
|------|--------|-------------|
| **0–10s** | Open Tab 1: Priority Queue | *"Cities get thousands of fragmented reports, but chronic underlying problems are buried across separate tickets."* |
| **10–20s** | Open Tab 2: Analyze Observation | *"Watch Gemma analyze this clogged storm drain. Notice how it extracts direct visible evidence, flags what it cannot see, and assigns severity."* |
| **20–30s** | Click **Run Triage** $\rightarrow$ **Enqueue** | *"It clusters this report into Block A, boosting the recurrence bonus."* |
| **30–40s** | Open Tab 3: Hotspot Map | *"Inspectors instantly see the multi-issue hotspot map and an explainable score breakdown—no black-box AI."* |
| **40–45s** | Conclude | *"CityPulse doesn't replace city inspectors—it helps them decide where to look first."* |

---

## 6. Project Structure

```
citypulse/
├── app.py                # Main Streamlit dashboard (Queue, Triage, Hotspot Map, Rehearsal)
├── sample_data.py        # Demo dataset, hotspot aggregation, priority formula
├── gemma_triage.py       # Multimodal extraction engine (Live API + Offline Fallback)
├── sample_images/        # Sample street frames for demonstration
├── requirements.txt      # Dependencies
└── README.md             # Project documentation and pitch guide
```
