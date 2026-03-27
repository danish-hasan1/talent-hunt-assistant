import sys

with open('app.py', 'r') as f:
    code = f.read()

# 1. Insert global top-right toggle for Landing Page
# Look for: if not st.session_state.get("user_email"):
auth_start = 'if not st.session_state.get("user_email"):'
auth_toggle = '''if not st.session_state.get("user_email"):
    col_logo, col_tgl = st.columns([9, 1])
    with col_tgl:
        is_dark = st.session_state.theme == "dark"
        if st.button("🌙" if is_dark else "🌞", key="theme_btn_landing"):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()
'''

code = code.replace(auth_start, auth_toggle)


# 2. Insert sidebar toggle for Internal Dashboard
# Look for:
# with st.sidebar:
#     st.title("Candidate Search")
sidebar_start = '''with st.sidebar:
    st.title("Candidate Search")
    st.caption("Zero-API sourcing engine")'''
sidebar_toggle = '''with st.sidebar:
    col_stitle, col_stgl = st.columns([8, 2])
    with col_stitle:
        st.title("Candidate Search")
        st.caption("Zero-API sourcing engine")
    with col_stgl:
        is_dark = st.session_state.theme == "dark"
        if st.button("🌙" if is_dark else "🌞", key="theme_btn_sidebar"):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()'''

code = code.replace(sidebar_start, sidebar_toggle)

with open('app.py', 'w') as f:
    f.write(code)
