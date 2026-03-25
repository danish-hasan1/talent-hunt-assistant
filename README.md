# Candidate Search Engine

Zero-API candidate sourcing engine — LinkedIn, GitHub, Naukri, Google X-ray.
Built on Streamlit + SQLite + Groq (Llama-3.3-70b).

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install webkit

# 2. Set your Groq API key
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# 3. Run
streamlit run app.py
```

## Project structure

```
candidate_search/
├── app.py                  # Streamlit entry point + nav
├── config.py               # API keys, DB path, constants
├── db.py                   # SQLite schema + all queries
├── jd_analysis.py          # 3-prompt chain (Prompt 1 + 2 + 3)
├── boolean_builder.py      # Filter → boolean string generator
├── pages/
│   └── search.py           # Two-mode search UI
└── requirements.txt
```

## How it works

### JD-driven mode
1. Paste a full job description
2. Click "Run analysis chain" — runs your 3 prompts via Groq
3. Filters auto-populate from the AI output
4. Review and adjust filters (add/remove skills, tweak location etc.)
5. Click "Search candidates" — fires scrapers across all sources

### Manual mode
Fill in filters directly and search without a JD.

### The 3-prompt chain
- **Prompt 1** — deep JD dissection: role intent, seniority, competencies, disqualifiers
- **Prompt 2** — weighted skills matrix (100-point scoring framework)
- **Prompt 3** — sourcing parameters: title variants, boolean strings (balanced/broad/narrow)

All 3 outputs are saved to the DB per job, so you can re-run or refine later.

## Next: connect your scrapers

In `pages/search.py`, find this comment:

```python
# TODO: trigger actual scraper here and populate st.session_state.results
```

Wire in your Playwright scrapers here. Each scraper should return a list of
candidate dicts matching the `candidates` table schema in `db.py`.

## Adding a candidate manually

```python
from db import upsert_candidate, link_candidate_to_job

candidate_id = upsert_candidate({
    "full_name": "Priya Sharma",
    "current_title": "Senior TA Lead",
    "current_company": "Infosys BPO",
    "location": "Bangalore",
    "linkedin_url": "https://linkedin.com/in/priya-sharma",
    "skills": ["RPO delivery", "Stakeholder management", "Workday"],
    "experience_years": 9,
    "source": "linkedin",
})

link_candidate_to_job(job_id=1, candidate_id=candidate_id, match_score=91.0)
```
