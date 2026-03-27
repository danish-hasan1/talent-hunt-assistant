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

from db import init_db, get_user, upsert_user, get_conn, create_user, verify_user_credentials
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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .tha-body { 
            font-family: 'Inter', sans-serif;
            padding-top: 2rem; 
            padding-bottom: 4rem; 
            color: #1e293b;
        }
        .tha-hero-title { 
            font-size: 3.5rem; 
            font-weight: 800; 
            margin-bottom: 1.5rem; 
            line-height: 1.1;
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .tha-hero-subtitle { 
            font-size: 1.25rem; 
            color: #475569; 
            margin-bottom: 2rem; 
            max-width: 680px; 
            line-height: 1.6;
            font-weight: 400;
        }
        .tha-pills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-bottom: 2rem;
        }
        .tha-pill { 
            display: inline-flex;
            align-items: center;
            padding: 0.4rem 1rem; 
            border-radius: 9999px; 
            background: rgba(37, 99, 235, 0.08); 
            color: #2563eb;
            font-size: 0.85rem; 
            font-weight: 600;
            border: 1px solid rgba(37, 99, 235, 0.15);
            transition: all 0.2s ease;
        }
        .tha-pill:hover {
            background: rgba(37, 99, 235, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1), 0 2px 4px -2px rgba(37, 99, 235, 0.1);
        }
        .tha-list-title {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            color: #1e293b;
        }
        .tha-list {
            list-style: none;
            padding: 0;
            margin: 0;
            margin-bottom: 2rem;
        }
        .tha-list li {
            position: relative;
            padding-left: 1.75rem;
            margin-bottom: 0.75rem;
            color: #475569;
            line-height: 1.5;
            font-size: 1.05rem;
        }
        .tha-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
        }
        
        /* Streamlit native container override */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.02) !important;
            border: 1px solid #e2e8f0 !important;
            background: #ffffff !important;
            transition: all 0.3s ease;
            overflow: hidden;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(-3px);
            border-color: #cbd5e1 !important;
        }
        
        .tha-feature-icon {
            font-size: 2.2rem;
            margin-bottom: 1.25rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.5rem;
            height: 3.5rem;
            background: #f8fafc;
            border-radius: 14px;
            border: 1px solid #f1f5f9;
            box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            transition: all 0.3s ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover .tha-feature-icon {
            background: #eff6ff;
            border-color: #dbeafe;
            transform: scale(1.05);
        }
        .tha-section-title { 
            font-size: 1.35rem; 
            font-weight: 700; 
            margin-bottom: 0.75rem; 
            color: #0f172a;
            letter-spacing: -0.01em;
        }
        .tha-feature-text { 
            color: #64748b; 
            font-size: 1.05rem; 
            line-height: 1.6;
        }
        
        hr.tha-divider {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
            margin: 4rem 0;
        }
        
        .tha-hiw-step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1.75rem;
            padding: 1rem;
            border-radius: 12px;
            transition: all 0.2s ease;
        }
        .tha-hiw-step:hover {
            background: #f8fafc;
        }
        .tha-hiw-number {
            flex-shrink: 0;
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 1.25rem;
            font-size: 1rem;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        }
        .tha-hiw-content {
            padding-top: 0.2rem;
            color: #475569;
            line-height: 1.6;
            font-size: 1.1rem;
        }
        .tha-hiw-content strong {
            color: #0f172a;
        }
        
        /* Subtle animation for the title gradient */
        .tha-hero-title {
            background-size: 200% auto;
            animation: textShine 5s linear infinite;
        }
        @keyframes textShine {
            to {
                background-position: 200% center;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='tha-body'>", unsafe_allow_html=True)
        hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])
        with hero_left:
            st.markdown("<div class='tha-hero-title'>Talent Hunt Assistant</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='tha-hero-subtitle'>Turn messy job descriptions into structured searches, reusable pipelines, and AI‑scored shortlists without handing everything to a third‑party ATS.</div>",
                unsafe_allow_html=True,
            )
            
            st.markdown("<div class='tha-list-title'>Built for senior recruiters and sourcing leads who:</div>", unsafe_allow_html=True)
            st.markdown(
                """
                <ul class='tha-list'>
                    <li>Want JD-driven, repeatable search setups instead of ad‑hoc strings.</li>
                    <li>Run multi‑region searches and need a single workspace to track them.</li>
                    <li>Prefer owning their own candidate database rather than renting access.</li>
                </ul>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<div class='tha-list-title' style='margin-top:2.5rem;'>Signals you control</div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class='tha-pills-container'>
                    <span class='tha-pill'>🎯 JD‑driven filters</span>
                    <span class='tha-pill'>🌐 Multi‑source X‑ray</span>
                    <span class='tha-pill'>🤖 AI scoring</span>
                    <span class='tha-pill'>📊 Per‑job pipeline</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        with hero_right:
            st.markdown("<div style='padding-top: 2rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<div style='padding: 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top: 0; color: #0f172a; font-weight: 700; font-family: Inter;'>Welcome 👋</h3>", unsafe_allow_html=True)
                st.caption("Create an account or sign in with your work email to access your private searches and API keys.")
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

                tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

                with tab_login:
                    login_email = st.text_input("Email", key="login_email", placeholder="name@company.com")
                    login_password = st.text_input("Password", key="login_password", type="password")
                    if st.button("Log in", key="login_btn", type="primary", use_container_width=True):
                        if not login_email.strip() or not login_password:
                            st.error("Enter both email and password.")
                        else:
                            user = verify_user_credentials(login_email.strip().lower(), login_password)
                            if not user:
                                st.error("Invalid email or password.")
                            else:
                                st.session_state.user_email = login_email.strip().lower()
                                st.rerun()

                with tab_signup:
                    signup_email = st.text_input("Work email", key="signup_email", placeholder="name@company.com")
                    signup_password = st.text_input("Password", key="signup_password", type="password")
                    signup_password2 = st.text_input("Confirm password", key="signup_password2", type="password")
                    if st.button("Create account", key="signup_btn", type="primary", use_container_width=True):
                        if not signup_email.strip() or not signup_password or not signup_password2:
                            st.error("Fill in all fields.")
                        elif signup_password != signup_password2:
                            st.error("Passwords do not match.")
                        else:
                            email_norm = signup_email.strip().lower()
                            try:
                                create_user(email_norm, signup_password)
                            except ValueError:
                                st.error("An account with this email already exists. Use Log in instead.")
                            else:
                                st.session_state.user_email = email_norm
                                st.rerun()

                st.markdown("<div style='text-align:center; margin-top:1.5rem;'><small style='color:#94a3b8; font-weight: 500;'>Your data remains within your environment.</small></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='tha-divider'>", unsafe_allow_html=True)

        feat_col1, feat_col2, feat_col3 = st.columns(3)
        with feat_col1:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>⚡</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Analyse any JD</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Break job descriptions into titles, skills, seniority and non‑negotiables with one click, then tweak filters like you would in a world‑class RPS.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        with feat_col2:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>🌍</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Source everywhere</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Generate X‑ray searches for LinkedIn, GitHub, Google and major regional job boards so you can directly target candidates where they actually are.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        with feat_col3:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>🏦</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Own your DB</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Save candidates once, attach them to multiple roles, track stages and match scores, and keep everything inside a unified database you control.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='tha-divider'>", unsafe_allow_html=True)

        how_col1, how_col2 = st.columns([1.1, 0.9])
        with how_col1:
            st.markdown("<div class='tha-section-title' style='margin-bottom: 2rem; font-size: 1.8rem;'>How it works</div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class='tha-hiw-step'>
                    <div class='tha-hiw-number'>1</div>
                    <div class='tha-hiw-content'><strong>Paste or load a JD</strong> and run analysis.</div>
                </div>
                <div class='tha-hiw-step'>
                    <div class='tha-hiw-number'>2</div>
                    <div class='tha-hiw-content'><strong>Review and adjust</strong> the auto‑generated filters.</div>
                </div>
                <div class='tha-hiw-step'>
                    <div class='tha-hiw-number'>3</div>
                    <div class='tha-hiw-content'><strong>Open suggested searches</strong> and add strong profiles to the pipeline.</div>
                </div>
                <div class='tha-hiw-step'>
                    <div class='tha-hiw-number'>4</div>
                    <div class='tha-hiw-content'><strong>Let AI score fit</strong> vs role, then drive outreach from your list.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with how_col2:
            st.markdown("<div style='padding: 1.5rem 0 0 2rem;'>", unsafe_allow_html=True)
            st.markdown("<div class='tha-section-title' style='margin-bottom: 1.5rem; font-size: 1.5rem;'>Why it stays yours</div>", unsafe_allow_html=True)
            st.info(
                "**Data Sovereignty First**\n\nAll data lives entirely in your localized environment. "
                "API keys are stored securely on a per-user basis, and the application seamlessly interfaces with your choice of commodity LLM providers "
                "(Groq, OpenAI, Anthropic, Gemini, Qwen). You remain independent, with zero vendor lock-in and complete control over your candidate intelligence."
            )
            st.markdown("</div>", unsafe_allow_html=True)

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

        if st.button("Log out"):
            for key in list(st.session_state.keys()):
                if key.startswith("f_") or key in (
                    "user_email",
                    "jd_text",
                    "filter_config",
                    "p1_out",
                    "p2_out",
                    "p3_out",
                    "job_id",
                    "search_done",
                    "results",
                    "search_links",
                ):
                    del st.session_state[key]
            st.rerun()

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
