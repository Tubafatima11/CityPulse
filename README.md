# CityPulse 🌆

**CityPulse** is an AI-powered urban infrastructure intelligence system that transforms everyday street imagery into actionable insights for smarter city maintenance. Powered by Gemma 4's multimodal capabilities, CityPulse analyzes street images and resident-reported descriptions to identify civic issues such as potholes, blocked drains, overflowing rubbish, damaged footpaths, and accessibility barriers.

The system extracts structured information from visual reports, identifies recurring issues using location-based grouping, and prioritizes observations through a transparent scoring algorithm based on severity, recurrence, and accessibility impact.

### ✨ Key Features

- **Multimodal AI Analysis:** Uses Gemma 4 to interpret street imagery and textual descriptions.
- **Structured Information Extraction:** Converts observations into structured JSON containing issue categories, visual evidence, severity, uncertainty, and recommended actions.
- **Duplicate Detection:** Groups potentially related reports to identify recurring infrastructure problems.
- **Intelligent Prioritization:** Ranks issues using an explainable, weighted scoring algorithm.
- **Interactive Dashboard:** Visualizes reported issues, recurring hotspots, priority rankings, and recommended inspection actions.
- **Evidence-Based Decisions:** Helps maintenance teams understand why an issue is flagged and what requires further verification.

### 🛠️ Tech Stack

- **AI Model:** Gemma 4
- **Programming Language:** Python
- **Frontend & Dashboard:** Streamlit
- **Data Format:** JSON
- **Analytics:** Rule-based scoring and location-based grouping

### 🎯 Vision

CityPulse aims to help cities move beyond fragmented complaint management toward proactive, evidence-driven infrastructure maintenance. By consolidating visual observations and highlighting recurring problems, it supports better inspection planning and more informed resource allocation.

**CityPulse doesn't replace human inspectors—it helps them identify where to look first.**

*Note: CityPulse is a prototype intended for AI-assisted infrastructure triage. Findings and priority scores require validation, and critical decisions should involve human inspection.*
