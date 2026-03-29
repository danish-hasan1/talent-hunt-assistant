import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from db import get_conn, delete_user
from theme import get_theme_css


st.set_page_config(
    page_title="THA Admin Portal",
    page_icon="🛠️",
    layout="wide",
)

# Inject the Neo-Minimalist SaaS Theme (No dark mode toggle needed, hardcoded in get_theme_css)
st.markdown(get_theme_css("light"), unsafe_allow_html=True)


st.title("Admin Portal")
st.caption("Warning: This portal is accessible via URL without authentication. Handle data with care.")

with get_conn() as conn:
    users = conn.execute("SELECT email, created_at FROM users ORDER BY created_at DESC").fetchall()
    jobs = conn.execute(
        "SELECT COUNT(*) AS c, COUNT(DISTINCT owner_email) AS owners FROM jobs"
    ).fetchone()
    candidates = conn.execute("SELECT COUNT(*) AS c FROM candidates").fetchone()
    job_cands = conn.execute("SELECT COUNT(*) AS c FROM job_candidates").fetchone()

# SaaS Cards for Metrics
with st.container(border=True):
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Total Users", len(users))
    with col_b:
        st.metric("Total Jobs Engagements", jobs["c"])
    with col_c:
        st.metric("Global Candidates", candidates["c"])
    with col_d:
        st.metric("Job–Candidate Links", job_cands["c"])

st.divider()
st.subheader("Manage Users")

with get_conn() as conn:
    user_rows = conn.execute(
        """
        SELECT u.email,
               u.created_at,
               COUNT(DISTINCT j.id) AS job_count,
               COUNT(DISTINCT jc.candidate_id) AS candidate_count
        FROM users u
        LEFT JOIN jobs j ON j.owner_email = u.email
        LEFT JOIN job_candidates jc ON jc.job_id = j.id
        GROUP BY u.email, u.created_at
        ORDER BY u.created_at DESC
        """
    ).fetchall()

if not user_rows:
    st.info("No users registered.")
else:
    for u in user_rows:
        with st.container(border=True):
            user_email = u['email']
            
            # Use columns to position the delete button safely on the right 
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{user_email}**")
                st.caption(f"Member since {u['created_at'][:10]}")
                st.caption(f"Jobs: {u['job_count']} | Sourced Candidates: {u['candidate_count']}")
            with c2:
                # Provide a quick confirmation toggle to prevent accidental clicks
                if st.button("Delete User", type="secondary", key=f"del_{user_email}"):
                    st.session_state[f"confirm_delete_{user_email}"] = True
                
                if st.session_state.get(f"confirm_delete_{user_email}"):
                    st.warning("Data will be lost!")
                    c_yes, c_no = st.columns(2)
                    with c_yes:
                        if st.button("Confirm", type="primary", key=f"yes_{user_email}"):
                            delete_user(user_email)
                            st.session_state[f"confirm_delete_{user_email}"] = False
                            st.rerun()
                    with c_no:
                        if st.button("Cancel", key=f"no_{user_email}"):
                            st.session_state[f"confirm_delete_{user_email}"] = False
                            st.rerun()
