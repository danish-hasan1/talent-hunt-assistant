import sys

def patch_app_py():
    with open('app.py', 'r') as f:
        code = f.read()

    # 1. Add Sidebar Disclaimer
    # Look for the st.sidebar.button("Log out") around line 413 or the end of the sidebar rendering in the login flow.
    # Actually, the sidebar rendering is inside the def main()
    # At the end of the sidebar in `main()`:
    sidebar_target = """        st.sidebar.markdown(
            f'<div style="{logout_btn_style}">Log out</div>', 
            unsafe_allow_html=True
        )"""
    
    sidebar_new = """        st.sidebar.markdown(
            f'<div style="{logout_btn_style}">Log out</div>', 
            unsafe_allow_html=True
        )

        st.sidebar.divider()
        st.sidebar.caption("⚠️ **Disclaimer:** Talent Hunt Assistant integrates with AI (LLMs) to enhance candidate sourcing. Always manually verify generated insights and search criteria before taking action.")"""
    
    if sidebar_target in code:
        code = code.replace(sidebar_target, sidebar_new)
    else:
        # Try finding the default streamlit button if styling was reverted or different
        if 'if st.button("Log out"):' in code:
            code = code.replace('if st.button("Log out"):', 'st.divider()\n        st.caption("⚠️ **Disclaimer:** Talent Hunt Assistant uses AI. Please verify all insights.")\n\n        if st.button("Log out"):')

    # 2. Settings API Guide
    settings_target = """        st.subheader("API keys")

        provider = st.selectbox("""
    
    settings_new = """        st.subheader("API keys")
        st.info("💡 **Welcome!** To activate the AI sourcing engine, you must provide an API key. We recommend **Groq** for extreme speed, or **OpenAI** for advanced reasoning.\\n\\n"
              "- [Get a FREE Groq API Key](https://console.groq.com/keys)\\n"
              "- [Get an OpenAI API Key](https://platform.openai.com/api-keys)\\n"
              "- [Get an Anthropic API Key](https://console.anthropic.com/settings/keys)\\n\\n"
              "Your keys are stored securely in your private local database.")

        provider = st.selectbox("""
    
    if settings_target in code:
        code = code.replace(settings_target, settings_new)
    
    with open('app.py', 'w') as f:
        f.write(code)


def patch_search_py():
    with open('search.py', 'r') as f:
        code = f.read()

    # 3. Search Page Blank-State Tutorial
    # We will insert it right after _init_state() and before the subheader "Candidate Search"
    # Actually, the file just starts defining the UI after _init_state().
    # Let's target the exact spot below _init_state()
    target = """def _reset_search():"""
    
    new_code = """from db import get_user
user_data = get_user(st.session_state.get("user_email")) if st.session_state.get("user_email") else {}
user_api_keys = user_data.get("api_keys") or {}

if not user_api_keys:
    st.markdown("### ⚠️ API Setup Required")
    st.markdown(
        \"\"\"
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
        \"\"\",
        unsafe_allow_html=True
    )
    st.stop()


def _reset_search():"""

    if target in code and "user_api_keys =" not in code:
        code = code.replace(target, new_code)
        with open('search.py', 'w') as f:
            f.write(code)

if __name__ == "__main__":
    patch_app_py()
    patch_search_py()
    print("Patched app.py and search.py")
