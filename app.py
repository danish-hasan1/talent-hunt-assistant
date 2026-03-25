"""
app.py — entry point for the candidate search engine.

Run with:
    streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv   # pip install python-dotenv

# Load .env file if present (GROQ_API_KEY, DB_PATH, etc.)
load_dotenv()

from db import init_db

st.set_page_config(
    page_title="Candidate Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ---------------------------------------------------------------------------
# Sidebar nav
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Candidate Search")
    st.caption("Zero-API sourcing engine")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Search", "Saved Jobs", "Candidate DB", "Settings"],
        label_visibility="collapsed",
    )

    st.divider()

    # Quick API key check
    from config import GROQ_API_KEY
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not set")
        st.caption("Set it in your .env file or environment:\n`export GROQ_API_KEY=gsk_...`")
    else:
        st.success("Groq connected")

# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
if page == "Search":
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location(
        "search_page",
        os.path.join(os.path.dirname(__file__), "search.py")
    )
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)                 # type: ignore

elif page == "Saved Jobs":
    from db import list_jobs, get_job
    st.title("Saved jobs")
    jobs = list_jobs()
    if not jobs:
        st.info("No saved jobs yet. Run a search to create one.")
    else:
        for job in jobs:
            with st.expander(f"{job['title']} — {job['status']} ({job['created_at'][:10]})"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    detail = get_job(job["id"])
                    fc = detail.get("filter_config") or {}
                    if fc:
                        st.caption(f"Titles: {', '.join(fc.get('titles', [])[:3])}")
                        st.caption(f"Location: {fc.get('location', '')}")
                        st.caption(f"Experience: {fc.get('exp_range', '')}")
                with col2:
                    if st.button("Open", key=f"open_{job['id']}"):
                        st.session_state.job_id = job["id"]
                        st.session_state.page = "Search"
                        st.rerun()

elif page == "Candidate DB":
    from db import get_conn
    st.title("Candidate database")
    search_q = st.text_input("Search candidates", placeholder="Name, title, skill...")
    with get_conn() as conn:
        if search_q:
            q = f"%{search_q}%"
            rows = conn.execute(
                """SELECT * FROM candidates
                   WHERE full_name LIKE ? OR current_title LIKE ? OR skills LIKE ?
                   ORDER BY created_at DESC LIMIT 100""",
                (q, q, q)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM candidates ORDER BY created_at DESC LIMIT 100"
            ).fetchall()

    st.caption(f"{len(rows)} candidates found")
    for r in rows:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{r['full_name'] or 'Unknown'}**")
                st.caption(f"{r['current_title'] or ''} @ {r['current_company'] or ''} — {r['location'] or ''}")
                if r["linkedin_url"]:
                    st.caption(f"[LinkedIn]({r['linkedin_url']})")
            with col2:
                st.caption(f"Source: {r['source'] or '—'}")
                st.caption(f"Added: {(r['created_at'] or '')[:10]}")

elif page == "Settings":
    st.title("Settings")

    st.subheader("API keys")
    groq_key = st.text_input("Groq API key",
                              value=os.environ.get("GROQ_API_KEY", ""),
                              type="password")
    if st.button("Save to .env"):
        with open(".env", "a") as f:
            f.write(f"\nGROQ_API_KEY={groq_key}")
        st.success("Saved to .env — restart the app to apply.")

    st.subheader("Database")
    from config import DB_PATH
    st.code(DB_PATH)

    st.subheader("Model")
    from config import GROQ_MODEL
    st.code(GROQ_MODEL)
