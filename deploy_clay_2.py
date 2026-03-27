import sys

def rewrite_vite_html():
    with open('landing-page/index.html', 'r') as f:
        html = f.read()
    
    # Add logo image to navbar
    html = html.replace('<span class="logo-icon">🔍</span>', '<img src="./logo.png" alt="Logo" class="logo-img" />')
    
    with open('landing-page/index.html', 'w') as f:
        f.write(html)

def remove_dark_mode_from_app():
    with open('app.py', 'r') as f:
        code = f.read()
    
    # Remove sidebar toggle
    target = """        is_dark = st.session_state.theme == "dark"
        if st.button("🌙" if is_dark else "🌞", key="theme_btn_sidebar"):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()"""
    
    if target in code:
        code = code.replace(target, '        st.markdown("<div style=\\"height: 38px;\\"></div>", unsafe_allow_html=True)')
    
    # Remove landing page toggle
    target_lp = """                is_dark = st.session_state.theme == "dark"
                if st.button("🌙" if is_dark else "🌞", key="theme_btn_landing"):
                    st.session_state.theme = "light" if is_dark else "dark"
                    st.rerun()"""
    if target_lp in code:
        code = code.replace(target_lp, '                st.markdown("<div style=\\"height: 38px;\\"></div>", unsafe_allow_html=True)')

    with open('app.py', 'w') as f:
        f.write(code)

if __name__ == "__main__":
    rewrite_vite_html()
    remove_dark_mode_from_app()
    print("HTML and app.py patched!")
