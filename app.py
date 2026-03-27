"""
app.py — entry point for the candidate search engine.

Run with:
    streamlit run app.py
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()

from db import init_db, get_user, upsert_user, get_conn
from jd_analysis import _parse_json

st.set_page_config(
    page_title="Candidate Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

owner_email = os.environ.get("THA_OWNER_EMAIL", "").strip().lower()
if owner_email and "user_email" not in st.session_state:
    st.session_state.user_email = owner_email

if not st.session_state.get("user_email"):
    st.markdown(
        """
        <style>
        .tha-body { padding-top: 2rem; padding-bottom: 3rem; }
        .tha-hero-title { font-size: 2.6rem; font-weight: 700; margin-bottom: 0.35rem; }
        .tha-hero-subtitle { font-size: 1.1rem; color: #6c757d; margin-bottom: 1.6rem; max-width: 640px; }
        .tha-pill { display:inline-block; padding:0.2rem 0.9rem; border-radius:999px; background:#f1f3f5; font-size:0.8rem; margin-right:0.4rem; margin-bottom:0.4rem;}
        .tha-section-title { font-size:1.1rem; font-weight:600; margin-bottom:0.4rem; }
        .tha-muted { color:#6c757d; font-size:0.9rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='tha-body'>", unsafe_allow_html=True)
        hero_left, hero_right = st.columns([3, 2])
        with hero_left:
            st.markdown("<div class='tha-hero-title'>Talent Hunt Assistant</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='tha-hero-subtitle'>Turn messy job descriptions into structured searches, reusable pipelines, and AI‑scored shortlists without handing everything to a third‑party ATS.</div>",
                unsafe_allow_html=True,
            )
            st.markdown("**Built for senior recruiters and sourcing leads who:**")
            st.markdown(
                "- Want JD-driven, repeatable search setups instead of ad‑hoc strings.\n"
                "- Run multi‑region searches and need a single workspace to track them.\n"
                "- Prefer owning their own candidate database rather than renting access."
            )
            st.markdown("")
            st.markdown("**Signals you control**")
            st.markdown(
                "<span class='tha-pill'>JD‑driven filters</span>"
                "<span class='tha-pill'>Multi‑source X‑ray</span>"
                "<span class='tha-pill'>AI scoring</span>"
                "<span class='tha-pill'>Per‑job pipeline</span>",
                unsafe_allow_html=True,
            )
        with hero_right:
            with st.container(border=True):
                st.markdown("#### Sign in")
                st.caption("Use your work email to keep API keys and searches separate.")
                email = st.text_input("Work email", key="landing_email")
                if st.button("Continue", type="primary") and email.strip():
                    user_email = email.strip().lower()
                    st.session_state.user_email = user_email
                    existing = get_user(user_email)
                    if not existing:
                        upsert_user(user_email, {}, "groq")
                    st.experimental_rerun()

        st.markdown("---")

        feat_col1, feat_col2, feat_col3 = st.columns(3)
        with feat_col1:
            st.markdown("<div class='tha-section-title'>Analyse any JD</div>", unsafe_allow_html=True)
            st.markdown(
                "<span class='tha-muted'>Break job descriptions into titles, skills, seniority and non‑negotiables with one click, then tweak filters like you would in a world‑class RPS.</span>",
                unsafe_allow_html=True,
            )
        with feat_col2:
            st.markdown("<div class='tha-section-title'>Source across the open web</div>", unsafe_allow_html=True)
            st.markdown(
                "<span class='tha-muted'>Generate X‑ray searches for LinkedIn, GitHub, Google and major regional job boards so you can work where candidates actually are.</span>",
                unsafe_allow_html=True,
            )
        with feat_col3:
            st.markdown("<div class='tha-section-title'>Own your candidate DB</div>", unsafe_allow_html=True)
            st.markdown(
                "<span class='tha-muted'>Save candidates once, attach them to multiple roles, track stages and match scores, and keep everything inside a database you control.</span>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        how_col1, how_col2 = st.columns([2, 3])
        with how_col1:
            st.markdown("**How it works**")
            st.markdown(
                "1. Paste or load a JD and run analysis.\n"
                "2. Review and adjust the auto‑generated filters.\n"
                "3. Open the suggested searches and add strong profiles into the pipeline.\n"
                "4. Let AI score fit vs role, then drive outreach from your own shortlist."
            )
        with how_col2:
            st.markdown("**Why it stays yours**")
            st.markdown(
                "<span class='tha-muted'>All data lives in your environment. API keys are stored per user, and the tool works with commodity LLM providers instead of locking you into one vendor.</span>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar nav
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Candidate Search")
    st.caption("Zero-API sourcing engine")
    st.divider()

    if "page" not in st.session_state:
        st.session_state.page = "Search"

    pages = ["Search", "Saved Jobs", "Candidate DB", "Settings"]
    if os.environ.get("THA_ADMIN_MODE") == "1":
        pages.append("Admin")

    page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.divider()

    current_email = st.session_state.get("user_email", "")
    if current_email:
        st.caption(f"Signed in as {current_email}")

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
    from db import list_jobs, get_job, get_job_candidates, update_job_filters

    def _job_code(job_id: int) -> str:
        return f"THA-{job_id:04d}"

    st.title("Saved jobs")
    jobs = list_jobs()
    if not jobs:
        st.info("No saved jobs yet. Run a search to create one.")
    else:
        for job in jobs:
            detail = get_job(job["id"])
            fc = detail.get("filter_config") or {}
            label = fc.get("search_label") or job["title"]
            role_title = job["title"] or "Untitled role"
            code = _job_code(job["id"])
            candidates = get_job_candidates(job["id"])
            shortlisted = [c for c in candidates if c.get("stage") == "shortlisted"]
            jd_text = (detail.get("jd_text") or "").strip()
            summary = jd_text.replace("\n", " ")
            if len(summary) > 240:
                summary = summary[:240].rsplit(" ", 1)[0] + "..."

            with st.container(border=True):
                st.markdown(f"**{code} · {role_title}**")
                st.caption(f"{job['status']} · {job['created_at'][:10]}")
                st.caption(f"Candidates: {len(candidates)} · Shortlisted: {len(shortlisted)}")

                col_main, col_actions = st.columns([3, 1])
                with col_main:
                    with st.expander("View details"):
                        if summary:
                            st.write(summary)
                        titles = ", ".join(fc.get("titles", [])[:3])
                        if titles:
                            st.caption(f"Titles: {titles}")
                        if fc.get("location"):
                            st.caption(f"Location: {fc['location']}")
                        if fc.get("exp_range"):
                            st.caption(f"Experience: {fc['exp_range']}")

                    if st.button("View analysis results", key=f"view_analysis_{job['id']}"):
                        st.session_state[f"show_analysis_{job['id']}"] = not st.session_state.get(
                            f"show_analysis_{job['id']}", False
                        )

                    if st.session_state.get(f"show_analysis_{job['id']}"):
                        with st.container(border=True):
                            st.markdown("**Analysis results**")
                            p1 = {}
                            p2 = {}
                            raw_p1 = detail.get("p1_analysis") or ""
                            raw_p2 = detail.get("p2_matrix") or ""
                            if raw_p1:
                                try:
                                    p1 = _parse_json(raw_p1)
                                except Exception:
                                    p1 = {}
                            if raw_p2:
                                try:
                                    p2 = _parse_json(raw_p2)
                                except Exception:
                                    p2 = {}

                            role_obj = p1.get("role_objective") or ""
                            if role_obj:
                                st.markdown(f"**Role objective**: {role_obj}")

                            prim = p1.get("primary_competencies") or []
                            if prim:
                                st.markdown("**Core competencies**")
                                for c in prim[:6]:
                                    name = c.get("name") or ""
                                    why = c.get("why_essential") or ""
                                    st.markdown(f"- **{name}** — {why}")

                            non_neg = p2.get("non_negotiables") or []
                            if non_neg:
                                st.markdown("**Non‑negotiables / gaps**")
                                for n in non_neg:
                                    st.markdown(f"- {n}")

                            if st.button("Load JD", key=f"load_{job['id']}"):
                                st.session_state.job_to_load = job["id"]
                                st.session_state.page = "Search"
                                st.rerun()

                with col_actions:
                    new_label = st.text_input("Search name", value=label, key=f"label_{job['id']}")
                    if new_label != label:
                        fc["search_label"] = new_label
                        update_job_filters(job["id"], fc, detail.get("boolean_string", "") or "")

elif page == "Candidate DB":
    from db import get_conn
    st.title("Candidate database")
    search_q = st.text_input("Search candidates", placeholder="Name, title, skill...")
    with get_conn() as conn:
        base_sql = """
            SELECT c.*, 
                   GROUP_CONCAT(j.title, ' | ') AS roles,
                   GROUP_CONCAT(j.id, ',') AS role_ids
            FROM candidates c
            LEFT JOIN job_candidates jc ON jc.candidate_id = c.id
            LEFT JOIN jobs j ON j.id = jc.job_id
            WHERE 1=1
        """
        params = []
        if search_q:
            base_sql += " AND (c.full_name LIKE ? OR c.current_title LIKE ? OR c.skills LIKE ?)"
            q = f"%{search_q}%"
            params.extend([q, q, q])
        base_sql += " GROUP BY c.id ORDER BY c.created_at DESC LIMIT 100"
        rows = conn.execute(base_sql, params).fetchall()

    st.caption(f"{len(rows)} candidates found")
    for r in rows:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{r['full_name'] or 'Unknown'}**")
                st.caption(f"{r['current_title'] or ''} @ {r['current_company'] or ''} — {r['location'] or ''}")
                if r["linkedin_url"]:
                    st.caption(f"[LinkedIn]({r['linkedin_url']})")
                if r["roles"]:
                    st.caption(f"Roles: {r['roles']}")
                if r["linkedin_pdf_path"]:
                    try:
                        with open(r["linkedin_pdf_path"], "rb") as f:
                            st.download_button(
                                "Download profile PDF",
                                data=f,
                                file_name=r["linkedin_pdf_path"].split("/")[-1],
                                mime="application/pdf",
                                key=f"pdf_{r['id']}",
                            )
                    except Exception:
                        pass
            with col2:
                st.caption(f"Source: {r['source'] or '—'}")
                st.caption(f"Added: {(r['created_at'] or '')[:10]}")

elif page == "Settings":
    st.title("Settings")

    st.subheader("Profile")
    user_email = st.session_state.get("user_email", "")
    if not user_email:
        st.info("You are not signed in. Refresh to go back to the landing page and enter your email.")
    else:
        user = get_user(user_email) or {"api_keys": {}, "preferred_provider": "groq"}
        api_keys = user.get("api_keys") or {}
        preferred_provider = user.get("preferred_provider") or "groq"

        col_p1, col_p2 = st.columns([2, 2])
        with col_p1:
            st.markdown(f"**Email**: {user_email}")
        with col_p2:
            st.markdown(f"**Preferred provider**: {preferred_provider or 'groq'}")

        st.divider()
        st.subheader("API keys")

        provider = st.selectbox(
            "Preferred provider",
            ["groq", "openai", "anthropic", "gemini", "qwen"],
            index=["groq", "openai", "anthropic", "gemini", "qwen"].index(preferred_provider)
            if preferred_provider in ["groq", "openai", "anthropic", "gemini", "qwen"]
            else 0,
        )

        groq_key = st.text_input("Groq API key", value=api_keys.get("groq", ""), type="password")
        openai_key = st.text_input("OpenAI API key", value=api_keys.get("openai", ""), type="password")
        anthropic_key = st.text_input("Anthropic API key", value=api_keys.get("anthropic", ""), type="password")
        gemini_key = st.text_input("Gemini API key", value=api_keys.get("gemini", ""), type="password")
        qwen_key = st.text_input("Qwen API key", value=api_keys.get("qwen", ""), type="password")

        if st.button("Save API keys"):
            new_keys = {
                "groq": groq_key.strip(),
                "openai": openai_key.strip(),
                "anthropic": anthropic_key.strip(),
                "gemini": gemini_key.strip(),
                "qwen": qwen_key.strip(),
            }
            upsert_user(user_email, new_keys, provider)
            st.success("API keys saved for this account.")

    st.subheader("Database")
    from config import DB_PATH
    st.code(DB_PATH)

    st.subheader("Model")
    from config import GROQ_MODEL
    st.code(GROQ_MODEL)

elif page == "Admin":
    st.title("Admin dashboard")
    with get_conn() as conn:
        users = conn.execute("SELECT email, api_keys, created_at FROM users ORDER BY created_at DESC").fetchall()
        jobs = conn.execute("SELECT COUNT(*) AS c FROM jobs").fetchone()["c"]
        candidates = conn.execute("SELECT COUNT(*) AS c FROM candidates").fetchone()["c"]
        job_cands = conn.execute("SELECT COUNT(*) AS c FROM job_candidates").fetchone()["c"]

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Users", len(users))
    with col_b:
        st.metric("Jobs", jobs)
    with col_c:
        st.metric("Candidates", candidates)
    with col_d:
        st.metric("Job–candidate links", job_cands)

    st.subheader("Users")
    for u in users:
        api_keys = {}
        if u["api_keys"]:
            try:
                api_keys = json.loads(u["api_keys"])
            except Exception:
                api_keys = {}
        providers = [k for k, v in api_keys.items() if v]
        with st.container(border=True):
            st.markdown(f"**{u['email']}**")
            st.caption(f"Providers configured: {', '.join(providers) or 'none'}")
            st.caption(f"Created: {u['created_at']}")
