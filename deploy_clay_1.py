import os
import shutil
import base64

LOGO_SRC = "/Users/danishhasan/.gemini/antigravity/brain/23d0d9e5-70ff-433c-8b19-5f923258dea6/talent_hunt_logo_1774652255822.png"
L_PAGE_PUBLIC = "/Users/danishhasan/Documents/Antigravity/Talent-Hunt-Assistant/landing-page/logo.png"

def deploy():
    # 1. Copy Logo
    shutil.copy2(LOGO_SRC, L_PAGE_PUBLIC)
    
    # 2. Get Base64 of Logo
    with open(LOGO_SRC, "rb") as f:
        b64_logo = base64.b64encode(f.read()).decode()

    # 3. Patch theme.py entirely to Claymorphism (No dark mode logic)
    theme_py_content = f'''def get_theme_css(theme: str) -> str:
    # THEME IGNORED: We are locking into a pristine Claymorphism Light Mode.
    clay_css = r"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global Theme Override for Streamlit */
    .stApp {{
        background-color: #E2E8F0 !important;
        color: #1E293B !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    
    /* Claymorphic Animated Background Orbs */
    .background-orbs {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        overflow: hidden; z-index: -1; pointer-events: none;
    }}
    .orb {{
        position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.6;
        animation: float 20s infinite alternate ease-in-out;
    }}
    .orb-1 {{ width: 600px; height: 600px; background: radial-gradient(circle, #5EEAD4, transparent 70%); top: -200px; right: -100px; }}
    .orb-2 {{ width: 500px; height: 500px; background: radial-gradient(circle, #99F6E4, transparent 70%); bottom: -100px; left: -200px; animation-delay: -5s; }}
    .orb-3 {{ width: 400px; height: 400px; background: radial-gradient(circle, #14B8A6, transparent 70%); top: 40%; left: 30%; animation-delay: -10s; opacity: 0.2; }}
    @keyframes float {{
        0% {{ transform: translate(0, 0) scale(1); }}
        100% {{ transform: translate(50px, 50px) scale(1.1); }}
    }}

    /* Global typography */
    .tha-body {{ 
        font-family: 'Outfit', sans-serif;
        padding-top: 2rem; 
        padding-bottom: 4rem; 
        color: #334155;
    }}
    
    /* Logo Integration in Sidebar Navbar */
    [data-testid="stSidebar"]::before {{
        content: '';
        display: block;
        width: 140px;
        height: 140px;
        margin: 1rem auto 2rem auto;
        background-image: url("data:image/png;base64,{b64_logo}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 30px;
        box-shadow: 8px 8px 16px #c8d0d8, -8px -8px 16px #ffffff;
    }}

    /* Native Streamlit Container Override - CLAYMORPHISM */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 24px !important;
        background: #E2E8F0 !important;
        border: none !important;
        box-shadow: 12px 12px 24px #cbd5e1, -12px -12px 24px #ffffff !important;
        transition: all 0.4s ease;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        box-shadow: 16px 16px 32px #cbd5e1, -16px -16px 32px #ffffff !important;
        transform: translateY(-2px);
    }}
    
    /* Search Pipeline Horizontal Links (.tha-search-link-btn) - CLAYMORPHISM */
    .tha-search-link-btn {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.6rem 1.25rem !important;
        background: #E2E8F0 !important;
        color: #0F766E !important;
        text-decoration: none !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 6px 6px 12px #cbd5e1, -6px -6px 12px #ffffff !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 2px solid transparent !important;
    }}
    .tha-search-link-btn:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 8px 8px 16px #cbd5e1, -8px -8px 16px #ffffff !important;
        color: #0D9488 !important;
    }}
    .tha-search-link-btn:active {{
        box-shadow: inset 4px 4px 8px #cbd5e1, inset -4px -4px 8px #ffffff !important;
        transform: translateY(1px) !important;
    }}

    /* Native Streamlit Buttons - CLAYMORPHISM */
    .stButton button {{
        background: #0D9488 !important;
        color: white !important;
        border: none !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        /* Outer glow/shadow for the primary button */
        box-shadow: 6px 6px 12px #cbd5e1, -6px -6px 12px #ffffff, inset 2px 2px 4px rgba(255,255,255,0.3) !important;
    }}
    .stButton button:hover {{
        transform: translateY(-2px) !important;
        background: #0F766E !important;
        box-shadow: 8px 8px 16px #cbd5e1, -8px -8px 16px #ffffff, inset 2px 2px 4px rgba(255,255,255,0.3) !important;
    }}
    .stButton button:active {{
        transform: translateY(1px) !important;
        box-shadow: inset 4px 4px 8px rgba(0,0,0,0.2) !important;
    }}
    
    /* Inputs / Text Areas / Selectboxes */
    .stTextInput input, .stPasswordInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {{
        background: #E2E8F0 !important;
        border: none !important;
        color: #1E293B !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: inset 4px 4px 8px #cbd5e1, inset -4px -4px 8px #ffffff !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
    }}
    .stTextInput input:focus, .stPasswordInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {{
        box-shadow: inset 6px 6px 12px #cbd5e1, inset -6px -6px 12px #ffffff, 0 0 0 2px rgba(13, 148, 136, 0.4) !important;
    }}
    
    /* Markdown Text Overrides */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown span {{
        color: #1E293B !important;
    }}
    .stMarkdown .stCaptionContainer p, .stMarkdown small, p[style*="color: #94A3B8"] {{
        color: #64748B !important;
    }}
    
    /* Native Checkboxes */
    .stCheckbox label span:first-child {{
        border-radius: 6px !important;
        border: none !important;
        background: #E2E8F0 !important;
        box-shadow: 2px 2px 5px #cbd5e1, -2px -2px 5px #ffffff !important;
    }}
    .stCheckbox label[data-checked="true"] span:first-child {{
        background: #0D9488 !important;
        box-shadow: inset 2px 2px 4px rgba(0,0,0,0.2) !important;
    }}

    /* --- Sidebar Navigation Overhaul --- */
    [data-testid="stSidebar"] {{
        background-color: #E2E8F0 !important;
        border-right: none !important;
        box-shadow: 10px 0 20px rgba(0,0,0,0.05) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex; flex-direction: column; gap: 0.75rem;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {{
        padding: 1rem 1.25rem !important;
        border-radius: 16px !important;
        background: #E2E8F0 !important;
        border: none !important;
        box-shadow: 6px 6px 12px #cbd5e1, -6px -6px 12px #ffffff !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important; width: 100%; margin-bottom: 0 !important; display: flex; align-items: center;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-of-type {{
        display: none !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important; font-size: 1.05rem !important; color: #64748B !important; margin: 0 !important; transition: color 0.3s ease !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {{
        background: #E2E8F0 !important; transform: translateX(4px); box-shadow: 8px 8px 16px #cbd5e1, -8px -8px 16px #ffffff !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover p {{ color: #0D9488 !important; }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {{
        background: #E2E8F0 !important;
        box-shadow: inset 6px 6px 12px #cbd5e1, inset -6px -6px 12px #ffffff !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {{
        color: #0F766E !important; font-weight: 700 !important;
    }}
    
    /* Inline code blocks / JSON preview */
    .stCodeBlock, pre {{
        border-radius: 16px !important;
        background: #E2E8F0 !important;
        border: none !important;
        box-shadow: inset 6px 6px 12px #cbd5e1, inset -6px -6px 12px #ffffff !important;
    }}
    
    /* Empty State Div override */
    div[style*="background: rgba(255, 255, 255, 0.03)"] {{
        background: #E2E8F0 !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 8px 8px 16px #cbd5e1, -8px -8px 16px #ffffff !important;
    }}
    div[style*="background: rgba(255, 255, 255, 0.03)"] h4, 
    div[style*="background: rgba(255, 255, 255, 0.03)"] ol {{
        color: #1E293B !important;
    }}

    </style>"""
    return clay_css
'''
    with open('theme.py', 'w') as f:
        f.write(theme_py_content)

if __name__ == "__main__":
    deploy()
    print("Base64 Generated and theme.py replaced with Claymorphism engine.")
