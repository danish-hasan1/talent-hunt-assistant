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

if "user_email" not in st.session_state and "user" in st.query_params:
    st.session_state.user_email = st.query_params["user"]

owner_email = os.environ.get("THA_OWNER_EMAIL", "").strip().lower()
if owner_email and "user_email" not in st.session_state:
    st.session_state.user_email = owner_email

if not st.session_state.get("user_email"):
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

        /* Global Theme Override for Streamlit */
        .stApp {
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Animated Background Orbs */
        .background-orbs {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            overflow: hidden; z-index: -1; pointer-events: none;
        }
        .orb {
            position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.5;
            animation: float 20s infinite alternate ease-in-out;
        }
        .orb-1 { width: 600px; height: 600px; background: radial-gradient(circle, #38BDF8, transparent 70%); top: -200px; right: -100px; }
        .orb-2 { width: 500px; height: 500px; background: radial-gradient(circle, #C084FC, transparent 70%); bottom: -100px; left: -200px; animation-delay: -5s; }
        .orb-3 { width: 400px; height: 400px; background: radial-gradient(circle, #4F46E5, transparent 70%); top: 40%; left: 30%; animation-delay: -10s; opacity: 0.3; }
        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(50px, 50px) scale(1.1); }
        }

        .tha-body { 
            font-family: 'Outfit', sans-serif;
            padding-top: 2rem; 
            padding-bottom: 4rem; 
            color: #F8FAFC;
        }
        .tha-hero-title { 
            font-size: 3.5rem; 
            font-weight: 800; 
            margin-bottom: 1.5rem; 
            line-height: 1.1;
            background: linear-gradient(to right, #38BDF8, #818CF8, #C084FC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            animation: textShine 5s linear infinite;
            letter-spacing: -0.02em;
        }
        @keyframes textShine { to { background-position: 200% center; } }
        
        .tha-hero-subtitle { 
            font-size: 1.25rem; 
            color: #94A3B8; 
            margin-bottom: 2rem; 
            max-width: 680px; 
            line-height: 1.6;
            font-weight: 300;
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
            background: rgba(255, 255, 255, 0.03); 
            color: #818CF8;
            font-size: 0.85rem; 
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .tha-pill:hover {
            transform: translateY(-2px);
            background: rgba(129, 140, 248, 0.15);
            border-color: rgba(129, 140, 248, 0.3);
        }
        .tha-list-title {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            color: #F8FAFC;
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
            color: #94A3B8;
            line-height: 1.5;
            font-size: 1.05rem;
        }
        .tha-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #38BDF8;
            font-weight: bold;
        }
        
        /* Streamlit native container override */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            transition: all 0.4s ease;
            overflow: hidden;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.6) !important;
            transform: translateY(-3px);
            border-color: rgba(255, 255, 255, 0.15) !important;
        }
        
        /* Native Streamlit Text Inputs */
        .stTextInput input, .stPasswordInput input {
            background: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.3s ease;
        }
        .stTextInput input:focus, .stPasswordInput input:focus {
            border-color: #818CF8 !important;
            box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
        }
        
        /* Native Streamlit Buttons */
        .stButton button {
            background: linear-gradient(135deg, #4F46E5, #818CF8) !important;
            color: white !important;
            border: none !important;
            border-radius: 9999px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.39) !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
        }
        
        /* Native Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent !important;
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            color: #94A3B8 !important;
            font-weight: 600;
            background: transparent !important;
            border-bottom-width: 2px !important;
            padding-bottom: 0.5rem !important;
            border-bottom-color: transparent !important;
        }
        .stTabs [aria-selected="true"] {
            color: #F8FAFC !important;
            border-bottom-color: #4F46E5 !important;
        }
        
        /* Typography overrides for internal markdown */
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #F8FAFC !important;
        }
        .stMarkdown .stCaptionContainer p {
            color: #94A3B8 !important;
        }
        
        .tha-feature-icon {
            font-size: 2.2rem;
            margin-bottom: 1.25rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.5rem;
            height: 3.5rem;
            background: rgba(192, 132, 252, 0.15);
            color: #C084FC;
            border-radius: 14px;
            border: 1px solid rgba(192, 132, 252, 0.3);
            transition: all 0.3s ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover .tha-feature-icon {
            transform: scale(1.05);
        }
        .tha-section-title { 
            font-size: 1.35rem; 
            font-weight: 700; 
            margin-bottom: 0.75rem; 
            color: #F8FAFC !important;
            letter-spacing: -0.01em;
        }
        .tha-feature-text { 
            color: #94A3B8; 
            font-size: 1.05rem; 
            line-height: 1.6;
        }
        
        hr.tha-divider {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
            margin: 4rem 0;
        }
        
        .tha-hiw-step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1.75rem;
            padding: 1rem;
            border-radius: 12px;
            transition: all 0.2s ease;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .tha-hiw-step:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        .tha-hiw-number {
            flex-shrink: 0;
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #4F46E5 0%, #38BDF8 100%);
            color: white !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 1.25rem;
            font-size: 1rem;
            box-shadow: 0 4px 10px rgba(56, 189, 248, 0.3);
        }
        .tha-hiw-content {
            padding-top: 0.2rem;
            color: #94A3B8;
            line-height: 1.6;
            font-size: 1.1rem;
        }
        .tha-hiw-content strong {
            color: #F8FAFC;
        }

        /* Raw Vite Structural Elements */
        .badge { display: inline-block; padding: 0.4rem 1rem; border-radius: 9999px; background: rgba(56, 189, 248, 0.1); color: #38BDF8; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(56, 189, 248, 0.2); margin-bottom: 2rem; }
        .hero-title { font-size: 4rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; color: #F8FAFC !important; margin-bottom: 1.5rem; }
        .hero-title br { display: block; }
        .gradient-text { background: linear-gradient(to right, #38BDF8, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-size: 200% auto; animation: shine 4s linear infinite; }
        .hero-subtitle { font-size: 1.25rem; color: #94A3B8 !important; font-weight: 300; max-width: 580px; line-height: 1.6; margin-bottom: 3rem; }
        
        .hero-visual-wrapper { position: relative; display: flex; justify-content: flex-start; align-items: center; margin-top: 2rem; min-height: 350px; }
        .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 2rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
        .preview-card { width: 100%; max-width: 350px; height: 280px; display: flex; flex-direction: column; gap: 1rem; transform: rotate(5deg) scale(1.05); animation: floatCard 6s infinite ease-in-out; margin-left: 2rem; }
        @keyframes floatCard { 0%, 100% { transform: rotate(5deg) translateY(0); } 50% { transform: rotate(4deg) translateY(-20px); } }
        .stat-card { position: absolute; top: -10%; left: 0%; padding: 1.5rem; z-index: 2; transform: rotate(-5deg); animation: floatStat 7s infinite ease-in-out; }
        @keyframes floatStat { 0%, 100% { transform: rotate(-5deg) translateY(0); } 50% { transform: rotate(-3deg) translateY(15px); } }
        .stat-number { font-size: 2.5rem; font-weight: 800; color: #38BDF8; line-height: 1; }
        .stat-label { font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem; }
        .code-line { height: 12px; border-radius: 6px; background: rgba(255, 255, 255, 0.1); }
        .w-80 { width: 80%; } .w-60 { width: 60%; } .w-40 { width: 40%; } .w-90 { width: 90%; } .w-70 { width: 70%; }
        .highlight { background: linear-gradient(90deg, #4F46E5, #C084FC); }
        
        .features-header { text-align: center; margin-bottom: 4rem; margin-top: 4rem; }
        .features-header h2 { font-size: 3rem; font-weight: 800; letter-spacing: -0.02em; color: #F8FAFC !important; }
        .gradient-text-alt { background: linear-gradient(to right, #C084FC, #F472B6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; margin-bottom: 4rem; }
        .feature-card { padding: 3rem 2rem; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;}
        .feature-card:hover { transform: translateY(-8px); border-color: rgba(255, 255, 255, 0.2); background: rgba(255, 255, 255, 0.05); }
        .feature-icon.bg-purple { background: rgba(192, 132, 252, 0.15); color: #C084FC; border: 1px solid rgba(192, 132, 252, 0.3); }
        .feature-icon.bg-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
        .feature-icon.bg-emerald { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .feature-card h3 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: #F8FAFC !important;}
        .feature-card p { color: #94A3B8; font-size: 1.05rem; }

        </style>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="background-orbs">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
        </div>
        <div class='tha-body'>
        """, unsafe_allow_html=True)
        hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])
        with hero_left:
            st.markdown("""
            <div class="badge">Version 2.0 Live ✨</div>
            <div class="hero-title">
                Intelligent <br/>
                <span class="gradient-text">Talent Sourcing</span>
            </div>
            <div class="hero-subtitle">
                Turn messy job descriptions into structured searches, reusable pipelines, and AI‑scored shortlists without handing everything to a third‑party ATS.
            </div>
            <div class="hero-visual-wrapper">
                <div class="glass-card stat-card">
                    <div class="stat-number">4x</div>
                    <div class="stat-label">Faster Sourcing</div>
                </div>
                <div class="glass-card preview-card">
                    <div class="code-line w-80"></div>
                    <div class="code-line w-60"></div>
                    <div class="code-line w-40 highlight"></div>
                    <div class="code-line w-90"></div>
                    <div class="code-line w-70"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
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
                                st.query_params["user"] = st.session_state.user_email
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
                                st.query_params["user"] = email_norm
                                st.rerun()

                st.markdown("<div style='text-align:center; margin-top:1.5rem;'><small style='color:#94a3b8; font-weight: 500;'>Your data remains within your environment.</small></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='tha-divider'>", unsafe_allow_html=True)

        st.markdown("""
        <div class="features-header">
            <h2>Everything you need, <span class="gradient-text-alt">nothing you don't.</span></h2>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="tha-feature-icon bg-purple">⚡</div>
                <h3>Analyse any JD</h3>
                <p>Break job descriptions into titles, skills, seniority and non‑negotiables with one click, then tweak filters like you would in a world‑class RPS.</p>
            </div>
            <div class="feature-card">
                <div class="tha-feature-icon bg-blue">🌍</div>
                <h3>Source everywhere</h3>
                <p>Generate X‑ray searches for LinkedIn, GitHub, Google and major regional job boards so you can directly target candidates where they actually are.</p>
            </div>
            <div class="feature-card">
                <div class="tha-feature-icon bg-emerald">🏦</div>
                <h3>Own your DB</h3>
                <p>Save candidates once, attach them to multiple roles, track stages and match scores, and keep everything inside a unified database you control.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        if st.button("Log out", use_container_width=True, type="secondary"):
            st.session_state.clear()
            if "user" in st.query_params:
                del st.query_params["user"]
            st.rerun()

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
