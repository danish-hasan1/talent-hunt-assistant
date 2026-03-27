"""
pages/search.py — Candidate search page for the Streamlit app.

Two modes:
  1. JD-driven  — paste/fetch a JD, run the 3-prompt chain, review/edit
                  auto-populated filters, then search.
  2. Manual     — fill in filters directly, search immediately.

Both modes validate required fields before allowing search to fire.
"""

import streamlit as st
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from jd_analysis     import run_chain, validate_jd
from boolean_builder import generate_all_strings, validate_filters
from db              import (
    init_db,
    create_job,
    update_job_chain_outputs,
    update_job_filters,
    get_job,
    get_job_candidates,
    list_jobs,
    upsert_candidate,
    link_candidate_to_job,
    update_candidate_stage,
    search_candidates_in_db,
)
from scraper         import run_scrapers_for_job
from scorer          import score_candidate_for_job


def _job_code(job_id: int) -> str:
    return f"THA-{job_id:04d}"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Candidate Search", layout="wide")
init_db()

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
def _init_state():
    defaults = {
        "mode":           "jd",          # "jd" | "manual"
        "jd_text":        "",
        "chain_done":     False,
        "chain_error":    None,
        "p1_out":         {},
        "p2_out":         {},
        "p3_out":         {},
        "filter_config":  {},
        "job_id":         None,
        "search_done":    False,
        "results":        [],
        # Editable filter fields (populated by chain or entered manually)
        "f_titles":       "",
        "f_must_skills":  [],
        "f_nice_skills":  [],
        "f_exp_range":    "",
        "f_seniority":    "",
        "f_location":     "",
        "f_industry":     "",
        "f_exclude":      [],
        "f_sources":      {
            "linkedin": True,
            "github":   True,
            "naukri":   True,
            "google":   True,
            "db_only":  False,
        },
        "f_work_type":        "",
        "f_notice_period":    "",
        "f_company_size":     "",
        "f_language":         "",
        "f_relocation_ok":    False,
        "f_visa_sponsorship": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

from db import get_user
user_data = get_user(st.session_state.get("user_email")) if st.session_state.get("user_email") else {}
user_api_keys = user_data.get("api_keys") or {}

if not user_api_keys:
    st.markdown("### ⚠️ API Setup Required")
    st.markdown(
        """
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 2rem; margin-top: 1rem;">
            <h4 style="margin-top: 0; color: #F8FAFC;">Welcome to Talent Hunt Assistant!</h4>
            <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
                Before you can start deeply analyzing Job Descriptions and sourcing candidates automatically, you need to connect the brain. 
                Follow these 3 quick steps to get started:
            </p>
            <ol style="color: #F8FAFC; line-height: 2;">
                <li><strong>Generate an API Key:</strong> We recommend <a href="https://console.groq.com/keys" target="_blank" style="color: #38BDF8;">Groq</a> (it's currently free and insanely fast).</li>
                <li><strong>Open Settings:</strong> Click the <strong>Settings</strong> button in the left sidebar menu.</li>
                <li><strong>Save your Key:</strong> Paste your newly generated key into the corresponding box and click "Save API keys".</li>
            </ol>
            <br/>
            <p style="color: #94A3B8; font-size: 0.95rem;"><em>Once you hit save, simply click back to the Search tab! Your keys are stored locally and privately for your eyes only.</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()


def _reset_search():
    """Clear search results when filters change."""
    st.session_state.search_done = False
    st.session_state.results = []


def _populate_filters_from_chain():
    """Copy chain output into editable session state filter fields."""
    fc = st.session_state.filter_config
    st.session_state.f_titles      = ", ".join(fc.get("titles", []))
    st.session_state.f_must_skills = fc.get("must_skills", [])
    st.session_state.f_nice_skills = fc.get("nice_skills", [])
    st.session_state.f_exp_range   = fc.get("exp_range", "")
    st.session_state.f_seniority   = fc.get("seniority", "")
    st.session_state.f_location    = fc.get("location", "")
    st.session_state.f_industry    = fc.get("industry", "")
    st.session_state.f_exclude     = fc.get("exclude", [])
    st.session_state.f_work_type   = fc.get("work_type", "")
    st.session_state.f_notice_period = fc.get("notice_period", "")
    st.session_state.f_company_size  = fc.get("company_size", "")
    st.session_state.f_language      = fc.get("language", "")
    st.session_state.f_relocation_ok = fc.get("relocation_ok", False)
    st.session_state.f_visa_sponsorship = fc.get("visa_sponsorship", False)


job_to_load = st.session_state.pop("job_to_load", None)
if job_to_load:
    job = get_job(job_to_load)
    if job:
        st.session_state.jd_text = job.get("jd_text", "")
        fc_loaded = job.get("filter_config") or {}
        st.session_state.filter_config = fc_loaded
        try:
            from jd_analysis import _parse_json as _parse_json_for_load
            if job.get("p1_analysis"):
                st.session_state.p1_out = _parse_json_for_load(job["p1_analysis"])
            if job.get("p2_matrix"):
                st.session_state.p2_out = _parse_json_for_load(job["p2_matrix"])
            if job.get("p3_params"):
                st.session_state.p3_out = _parse_json_for_load(job["p3_params"])
        except Exception:
            st.session_state.p1_out = {}
            st.session_state.p2_out = {}
            st.session_state.p3_out = {}
        st.session_state.job_id = job_to_load
        st.session_state.chain_done = True
        st.session_state.chain_error = None
        _populate_filters_from_chain()
        _reset_search()


def _current_filter_config() -> dict:
    """Build a filter config dict from current session state fields."""
    existing_fc = st.session_state.get("filter_config") or {}
    search_label = existing_fc.get("search_label", "")
    titles = [t.strip() for t in st.session_state.f_titles.split(",") if t.strip()]
    return {
        "titles":      titles,
        "must_skills": st.session_state.f_must_skills,
        "nice_skills": st.session_state.f_nice_skills,
        "exp_range":   st.session_state.f_exp_range,
        "seniority":   st.session_state.f_seniority,
        "location":    st.session_state.f_location,
        "industry":    st.session_state.f_industry,
        "exclude":     st.session_state.f_exclude,
        "sources":     st.session_state.f_sources,
        "work_type":   st.session_state.f_work_type,
        "notice_period": st.session_state.f_notice_period,
        "company_size":  st.session_state.f_company_size,
        "language":      st.session_state.f_language,
        "relocation_ok": st.session_state.f_relocation_ok,
        "visa_sponsorship": st.session_state.f_visa_sponsorship,
        "search_label": search_label,
    }


# ---------------------------------------------------------------------------
# Mode toggle
# ---------------------------------------------------------------------------

st.title("Candidate search")

col_jd, col_manual = st.columns(2)
with col_jd:
    if st.button("JD-driven search",
                 type="primary" if st.session_state.mode == "jd" else "secondary",
                 use_container_width=True):
        st.session_state.mode = "jd"
        _reset_search()

with col_manual:
    if st.button("Manual search",
                 type="primary" if st.session_state.mode == "manual" else "secondary",
                 use_container_width=True):
        st.session_state.mode = "manual"
        _reset_search()

st.divider()


# ===========================================================================
# MODE 1 — JD-DRIVEN
# ===========================================================================

if st.session_state.mode == "jd":

    with st.expander("Load existing search", expanded=False):
        jobs = list_jobs()
        if jobs:
            options = [f"{_job_code(j['id'])} · {j['title']}" for j in jobs]
            selected = st.selectbox("Saved searches", options, index=0)
            if st.button("Load search"):
                job = next(j for j in jobs if f"{_job_code(j['id'])} · {j['title']}" == selected)
                detail = get_job(job["id"])
                st.session_state.jd_text = detail.get("jd_text", "")
                st.session_state.filter_config = detail.get("filter_config") or {}
                try:
                    if detail.get("p1_analysis"):
                        st.session_state.p1_out = json.loads(detail["p1_analysis"])
                    if detail.get("p2_matrix"):
                        st.session_state.p2_out = json.loads(detail["p2_matrix"])
                    if detail.get("p3_params"):
                        st.session_state.p3_out = json.loads(detail["p3_params"])
                except Exception:
                    st.session_state.p1_out = {}
                    st.session_state.p2_out = {}
                    st.session_state.p3_out = {}
                st.session_state.job_id = job["id"]
                st.session_state.chain_done = True
                st.session_state.chain_error = None
                _populate_filters_from_chain()
                _reset_search()
                st.rerun()

    with st.expander("Step 1 — Job description", expanded=not st.session_state.chain_done):

        jd_tab1, jd_tab2 = st.tabs(["Paste JD", "Fetch from URL"])

        with jd_tab1:
            st.session_state.jd_text = st.text_area(
                "Paste the full job description",
                value=st.session_state.jd_text,
                height=240,
                placeholder="Paste the complete job description here...",
                label_visibility="collapsed",
            )

        with jd_tab2:
            jd_url = st.text_input("Job posting URL",
                                   placeholder="https://company.com/careers/job-id")
            if st.button("Fetch JD from URL") and jd_url:
                with st.spinner("Fetching job description..."):
                    try:
                        # Playwright fetch — reuse your existing scraper
                        from scraper import fetch_jd_text  # type: ignore
                        st.session_state.jd_text = fetch_jd_text(jd_url)
                        st.success("JD fetched successfully.")
                    except ImportError:
                        st.warning("scraper.py not found — paste the JD manually for now.")
                    except Exception as e:
                        st.error(f"Fetch failed: {e}")

        # Validation warnings
        if st.session_state.jd_text:
            warnings = validate_jd(st.session_state.jd_text)
            for w in warnings:
                st.warning(w)

    with st.expander("Step 2 — Analyse with AI",
                     expanded=bool(st.session_state.jd_text) and not st.session_state.chain_done):

        # Progress display (only shown after run starts)
        if st.session_state.chain_done:
            st.success("Analysis complete — filters populated in Step 3.")
        elif st.session_state.chain_error:
            st.error(st.session_state.chain_error)

        can_run = bool(st.session_state.jd_text and
                       len(st.session_state.jd_text.strip()) > 80)

        if not can_run:
            st.info("Paste a job description above to enable analysis.")

        if st.button("Run analysis",
                     disabled=not can_run,
                     type="primary"):

            st.session_state.chain_done  = False
            st.session_state.chain_error = None
            _reset_search()

            progress_bar  = st.progress(0)
            status_text   = st.empty()

            step_labels = {
                1: "Understanding the role and intent...",
                2: "Building the skills and competency model...",
                3: "Deriving sourcing parameters and search strategy...",
            }

            def on_step(step: int, label: str):
                progress_bar.progress(step / 3)
                status_text.write(f"✓ {label}")

            with st.spinner("Running analysis — this takes ~15 seconds..."):
                result = run_chain(
                    st.session_state.jd_text,
                    on_step=on_step,
                )

            if result["error"]:
                st.session_state.chain_error = result["error"]
                st.error(result["error"])
            else:
                st.session_state.p1_out        = result["p1"]
                st.session_state.p2_out        = result["p2"]
                st.session_state.p3_out        = result["p3"]
                st.session_state.filter_config = result["filter_config"]
                st.session_state.chain_done    = True
                _populate_filters_from_chain()

                # Save to DB
                titles_for_job = result["filter_config"].get("titles") or []
                if titles_for_job:
                    job_title = titles_for_job[0]
                else:
                    job_title = "New job"
                job_id = create_job(
                    title=job_title,
                    jd_text=st.session_state.jd_text,
                    owner_email=st.session_state.get("user_email"),
                )
                update_job_chain_outputs(
                    job_id,
                    p1=result["p1_raw"],
                    p2=result["p2_raw"],
                    p3=result["p3_raw"],
                )
                st.session_state.job_id = job_id
                progress_bar.progress(1.0)
                status_text.write("✓ Analysis complete")
                st.rerun()

        if st.session_state.chain_done:
            with st.expander("Role understanding"):
                p1 = st.session_state.p1_out or {}
                role_obj = p1.get("role_objective") or ""
                seniority = p1.get("seniority_level") or ""
                ownership = p1.get("ownership_level") or ""
                ideal = p1.get("ideal_candidate_brief") or ""
                if role_obj:
                    st.markdown(f"**Role objective**: {role_obj}")
                if seniority or ownership:
                    st.markdown(f"**Seniority**: {seniority or '—'} &nbsp;&nbsp; **Ownership**: {ownership or '—'}")
                prim = p1.get("primary_competencies") or []
                if prim:
                    st.markdown("**Primary competencies**")
                    for c in prim:
                        name = c.get("name") or ""
                        why = c.get("why_essential") or ""
                        st.markdown(f"- **{name}** — {why}")
                sec = p1.get("secondary_competencies") or []
                if sec:
                    st.markdown("**Secondary competencies**")
                    st.markdown(", ".join(sec))
                disq = p1.get("disqualifiers") or []
                if disq:
                    st.markdown("**Disqualifiers**")
                    for d in disq:
                        st.markdown(f"- {d}")
                if ideal:
                    st.markdown("**Ideal candidate**")
                    st.markdown(ideal)

            with st.expander("Skills and competency model"):
                p2 = st.session_state.p2_out or {}
                matrix = p2.get("skills_matrix") or []
                if matrix:
                    sorted_matrix = sorted(matrix, key=lambda x: x.get("weight", 0), reverse=True)
                    top = sorted_matrix[:8]
                    st.markdown("**Key skills and weights**")
                    for item in top:
                        skill = item.get("skill") or ""
                        cat = item.get("category") or ""
                        wt = item.get("weight") or 0
                        st.markdown(f"- **{skill}** ({cat}, {wt} pts)")
                non_neg = p2.get("non_negotiables") or []
                if non_neg:
                    st.markdown("**Non‑negotiables**")
                    for n in non_neg:
                        st.markdown(f"- {n}")


# ===========================================================================
# FILTER PANEL — shared by both modes (JD-driven auto-populates, manual = blank)
# ===========================================================================

st.subheader("Search filters")

if st.session_state.mode == "jd" and st.session_state.chain_done:
    st.caption("AI-populated from your JD — edit freely before searching.")
elif st.session_state.mode == "jd":
    st.caption("Run the analysis chain above to auto-populate these filters.")

# ---- Required fields ------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.session_state.f_titles = st.text_input(
        "Job titles *(required)*",
        value=st.session_state.f_titles,
        placeholder="RPO Delivery Manager, Head of Talent, TA Lead",
        on_change=_reset_search,
    )

with col2:
    st.session_state.f_exp_range = st.text_input(
        "Experience range *(required)*",
        value=st.session_state.f_exp_range,
        placeholder="e.g. 8–14 years",
        on_change=_reset_search,
    )

st.session_state.f_location = st.text_input(
    "Location *(required)*",
    value=st.session_state.f_location,
    placeholder="e.g. Bangalore, Hyderabad, remote India",
    on_change=_reset_search,
)

# ---- Skills ---------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    current_must = st.session_state.f_must_skills or []
    new_must_skill = st.text_input("Must-have skills (comma-separated)",
                                   value=", ".join(current_must),
                                   placeholder="Braking systems, vehicle dynamics, test planning")
    skills_list = [s.strip() for s in new_must_skill.split(",") if s.strip()]
    if skills_list != current_must:
        st.session_state.f_must_skills = skills_list
        _reset_search()

with col4:
    current_nice = st.session_state.f_nice_skills or []
    new_nice_skill = st.text_input("Nice-to-have skills (comma-separated)",
                                   value=", ".join(current_nice),
                                   placeholder="Data analysis, English proficiency")
    skills_list_nice = [s.strip() for s in new_nice_skill.split(",") if s.strip()]
    if skills_list_nice != current_nice:
        st.session_state.f_nice_skills = skills_list_nice
        _reset_search()

# ---- Optional fields ------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    seniority_options = [
        "",
        "Intern / Trainee",
        "Junior (0–2)",
        "Mid-level (2–5)",
        "Senior (5–10)",
        "Lead / Principal",
        "Manager",
        "Senior Manager",
        "Director",
        "Senior Director",
        "VP",
        "SVP / EVP",
        "C-Suite / Partner",
        "Head / Global Head",
    ]
    cur_sen = st.session_state.f_seniority
    sen_idx = seniority_options.index(cur_sen) if cur_sen in seniority_options else 0
    st.session_state.f_seniority = st.selectbox(
        "Seniority", seniority_options, index=sen_idx, on_change=_reset_search
    )

with col6:
    st.session_state.f_industry = st.text_input(
        "Industry / background",
        value=st.session_state.f_industry,
        placeholder="e.g. RPO, MSP, In-house TA",
        on_change=_reset_search,
    )

col7, col8 = st.columns(2)

with col7:
    work_types = ["", "Remote", "Hybrid", "On-site"]
    cur_work = st.session_state.f_work_type
    work_idx = work_types.index(cur_work) if cur_work in work_types else 0
    st.session_state.f_work_type = st.selectbox(
        "Work type", work_types, index=work_idx, on_change=_reset_search
    )

with col8:
    notice_options = ["", "Immediate", "15 days", "30 days", "45 days", "60 days", "90 days"]
    cur_notice = st.session_state.f_notice_period
    notice_idx = notice_options.index(cur_notice) if cur_notice in notice_options else 0
    st.session_state.f_notice_period = st.selectbox(
        "Notice period", notice_options, index=notice_idx, on_change=_reset_search
    )

col9, col10 = st.columns(2)

with col9:
    size_options = [
        "",
        "Startup (1–50)",
        "Scale-up (51–200)",
        "Mid-size (201–1000)",
        "Large (1001–5000)",
        "Enterprise (5000+)",
    ]
    cur_size = st.session_state.f_company_size
    size_idx = size_options.index(cur_size) if cur_size in size_options else 0
    st.session_state.f_company_size = st.selectbox(
        "Target company size", size_options, index=size_idx, on_change=_reset_search
    )

with col10:
    st.session_state.f_language = st.text_input(
        "Language requirement",
        value=st.session_state.f_language,
        placeholder="e.g. French, German",
        on_change=_reset_search,
    )

col11, col12 = st.columns(2)

with col11:
    st.session_state.f_relocation_ok = st.checkbox(
        "Open to relocation required",
        value=st.session_state.f_relocation_ok,
    )

with col12:
    st.session_state.f_visa_sponsorship = st.checkbox(
        "Visa sponsorship required",
        value=st.session_state.f_visa_sponsorship,
    )

# ---- Exclusions -----------------------------------------------------------
current_excl = st.session_state.f_exclude or []
new_excl = st.multiselect(
    "Exclude terms",
    options=current_excl,
    default=current_excl,
)
new_excl_term = st.text_input("Add exclusion term", key="add_excl",
                               placeholder="e.g. agency recruiter, trainee")
if new_excl_term and new_excl_term not in st.session_state.f_exclude:
    st.session_state.f_exclude.append(new_excl_term)
    _reset_search()
    st.rerun()
st.session_state.f_exclude = new_excl

# ---- Sources --------------------------------------------------------------
st.markdown("**Search sources**")
src_cols = st.columns(5)
source_labels = {
    "linkedin": "LinkedIn",
    "github":   "GitHub",
    "naukri":   "Naukri / Indeed",
    "google":   "Google X-ray",
    "db_only":  "Existing DB only",
}
for i, (k, label) in enumerate(source_labels.items()):
    with src_cols[i]:
        st.session_state.f_sources[k] = st.checkbox(
            label,
            value=st.session_state.f_sources[k],
            key=f"src_{k}",
        )

# ---- Boolean preview ------------------------------------------------------
fc = _current_filter_config()
if fc.get("titles") or fc.get("must_skills"):
    boolean_strings = generate_all_strings(fc)
    with st.expander("Boolean search strings (auto-generated)"):
        st.markdown("**Balanced (default)**")
        st.code(boolean_strings["linkedin_balanced"], language="text")
        st.markdown("**Broad** — maximum discovery")
        st.code(boolean_strings["linkedin_broad"], language="text")
        st.markdown("**Narrow** — high precision")
        st.code(boolean_strings["linkedin_narrow"], language="text")
        st.markdown("**GitHub X-ray**")
        st.code(boolean_strings["github"], language="text")

# ---- Non-negotiables warning (from Prompt 2) ------------------------------
non_neg = st.session_state.filter_config.get("non_negotiables", [])
if non_neg:
    with st.expander(f"Non-negotiable conditions ({len(non_neg)}) — candidates missing these should be rejected"):
        for nn in non_neg:
            st.markdown(f"- {nn}")

st.divider()

# ---- SEARCH BUTTON --------------------------------------------------------
missing_fields = validate_filters(fc)

if missing_fields:
    for m in missing_fields:
        st.warning(f"Required: {m}")

search_clicked = st.button(
    "Search candidates",
    type="primary",
    disabled=bool(missing_fields),
    use_container_width=True,
)

if search_clicked and not missing_fields:
    if st.session_state.job_id:
        boolean_strings = generate_all_strings(fc)
        update_job_filters(
            st.session_state.job_id,
            filter_config=fc,
            boolean_string=boolean_strings["linkedin_balanced"],
        )

    st.session_state.search_done = True
    db_query = ", ".join(fc.get("titles", [])[:2])
    db_filters = {}
    if fc.get("location"):
        db_filters["location"] = fc["location"]
    if fc.get("exp_range"):
        import re
        m = re.search(r"(\d+)", fc["exp_range"])
        if m:
            db_filters["min_exp"] = int(m.group(1))

    results = search_candidates_in_db(db_query, db_filters)

    sources = fc.get("sources", {})
    search_links = []
    if any(sources.get(k) for k in ("linkedin", "github", "naukri", "google")):
        search_links = run_scrapers_for_job(st.session_state.job_id, fc)

    st.session_state.results = results
    st.session_state.search_links = search_links
    if not results:
        st.info("Search triggered. Review the AI matches below or explore candidates instantly using the generated external pipeline links.")

links = st.session_state.get("search_links") or []
if links:
    html_str = "<div style='display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem; justify-content: center;'>"
    for item in links:
        label = item.get("label", "Search")
        url = item.get("url", "")
        if url:
            icon = "↗"
            if "LinkedIn" in label: icon = "💼"
            elif "GitHub" in label: icon = "💻"
            elif "Google" in label: icon = "🔍"
            html_str += f"<a class='tha-search-link-btn' href='{url}' target='_blank'>{icon} {label}</a>"
    html_str += "</div>"
    st.markdown(html_str, unsafe_allow_html=True)


# ===========================================================================
# RESULTS
# ===========================================================================

if st.session_state.search_done:
    st.subheader("Results")

    tab_ranked, tab_bool, tab_pipeline = st.tabs(
        ["Ranked matches", "Boolean / raw results", "Pipeline"]
    )

    with tab_ranked:
        if st.session_state.job_id:
            with st.expander("Add candidate from LinkedIn URL"):
                with st.form("add_candidate_form"):
                    li_url = st.text_input("LinkedIn profile URL", placeholder="https://www.linkedin.com/in/...")
                    name = st.text_input("Full name")
                    title = st.text_input("Current title")
                    company = st.text_input("Current company")
                    location_val = st.text_input("Location", value=st.session_state.f_location)
                    skills_text = st.text_input("Skills (comma-separated)")
                    submitted = st.form_submit_button("Save to pipeline")
                if submitted and li_url:
                    skills_list = [s.strip() for s in skills_text.split(",") if s.strip()]
                    data = {
                        "full_name": name or None,
                        "current_title": title or None,
                        "current_company": company or None,
                        "location": location_val or None,
                        "email": None,
                        "phone": None,
                        "linkedin_url": li_url,
                        "github_url": None,
                        "profile_summary": "",
                        "skills": skills_list,
                        "experience_years": None,
                        "source": "manual_linkedin",
                        "source_url": li_url,
                        "raw_profile": "",
                    }
                    candidate_id = upsert_candidate(data)
                    job = get_job(st.session_state.job_id)
                    filter_config_for_score = (job or {}).get("filter_config") or fc
                    score, breakdown = score_candidate_for_job(filter_config_for_score, data)
                    link_candidate_to_job(
                        st.session_state.job_id,
                        candidate_id,
                        match_score=score,
                        score_breakdown=breakdown,
                    )
                    st.session_state.results = get_job_candidates(st.session_state.job_id)
                    st.success("Candidate added to pipeline for this job with AI match score.")
                    st.rerun()

        results = st.session_state.results
        if not results:
            st.info(
                "No in-app results yet. Use the Boolean / raw results tab and the opened browser searches "
                "to iteratively relax titles, skills, or locations until you see viable candidates."
            )
        else:
            for c in results:
                with st.container(border=True):
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    with col_a:
                        st.markdown(f"**{c.get('full_name', 'Unknown')}**")
                        st.caption(f"{c.get('current_title','')} @ {c.get('current_company','')}")
                        skills = c.get("skills", [])
                        if skills:
                            st.caption("Skills: " + " · ".join(skills[:6]))
                    with col_b:
                        score = c.get("match_score", 0)
                        color = "green" if score >= 80 else "orange" if score >= 60 else "red"
                        st.markdown(f":{color}[**{score:.0f}/100**]")
                    with col_c:
                        stage = st.selectbox(
                            "Stage",
                            ["found", "shortlisted", "contacted", "responded", "rejected"],
                            key=f"stage_{c.get('id')}",
                        )
                        if st.session_state.job_id and c.get("id"):
                            update_candidate_stage(
                                st.session_state.job_id,
                                c["id"],
                                stage,
                            )

    with tab_bool:
        if fc.get("titles") or fc.get("must_skills"):
            boolean_strings = generate_all_strings(fc)
            st.markdown("Copy these into Google or LinkedIn search:")
            st.code(boolean_strings["linkedin_balanced"], language="text")
            st.code(boolean_strings["linkedin_broad"],    language="text")
            st.code(boolean_strings["linkedin_narrow"],   language="text")

        else:
            st.info("Fill in filters above to generate boolean strings.")

    with tab_pipeline:
        if st.session_state.job_id:
            pipeline_candidates = get_job_candidates(st.session_state.job_id)
            stages = ["found", "shortlisted", "contacted", "responded", "rejected"]
            stage_cols = st.columns(len(stages))
            for i, stage in enumerate(stages):
                with stage_cols[i]:
                    in_stage = [c for c in pipeline_candidates if c.get("stage") == stage]
                    st.markdown(f"**{stage.title()}** ({len(in_stage)})")
                    for c in in_stage:
                        st.caption(c.get("full_name", "Unknown"))
        else:
            st.info("Pipeline tracking will appear here once a job is saved.")
