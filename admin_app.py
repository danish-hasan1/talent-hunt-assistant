import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from db import get_conn


st.set_page_config(
    page_title="THA Admin",
    page_icon="🛠️",
    layout="wide",
)


admin_password = os.environ.get("THA_ADMIN_PASSWORD", "")


def require_admin():
    if not admin_password:
        st.error("THA_ADMIN_PASSWORD is not set on this deployment.")
        st.stop()
    if not st.session_state.get("is_admin"):
        pw = st.text_input("Admin password", type="password")
        if st.button("Enter") and pw == admin_password:
            st.session_state.is_admin = True
            st.experimental_rerun()
        st.stop()


require_admin()


st.title("Talent Hunt Assistant — Admin")

with get_conn() as conn:
    users = conn.execute("SELECT email, created_at FROM users ORDER BY created_at DESC").fetchall()
    jobs = conn.execute(
        "SELECT COUNT(*) AS c, COUNT(DISTINCT owner_email) AS owners FROM jobs"
    ).fetchone()
    candidates = conn.execute("SELECT COUNT(*) AS c FROM candidates").fetchone()
    job_cands = conn.execute("SELECT COUNT(*) AS c FROM job_candidates").fetchone()

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric("Users", len(users))
with col_b:
    st.metric("Jobs", jobs["c"])
with col_c:
    st.metric("Candidates", candidates["c"])
with col_d:
    st.metric("Job–candidate links", job_cands["c"])

st.markdown("---")

st.subheader("Users")

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

for u in user_rows:
    with st.container(border=True):
        st.markdown(f"**{u['email']}**")
        st.caption(f"Created: {u['created_at']}")
        st.caption(f"Jobs: {u['job_count']} · Unique candidates: {u['candidate_count']}")

