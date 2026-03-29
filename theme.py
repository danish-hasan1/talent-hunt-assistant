def get_theme_css(theme: str) -> str:
    # REFACTORED: Modern Neo-Minimalist SaaS Aesthetic
    saas_css = r"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        /* Core Colors */
        --bg-main: #f1f5f9;
        --bg-surface: #ffffff;
        --primary: #10b981;
        --primary-hover: #059669;
        
        /* Text Colors */
        --text-heading: #0f172a;
        --text-body: #475569;
        --text-muted: #94a3b8;
        
        /* Borders & Shadows */
        --border-light: #e2e8f0;
        --shadow-soft: 0 4px 12px rgba(0,0,0,0.03), 0 1px 3px rgba(0,0,0,0.05);
        --radius-card: 14px;
        --radius-btn: 10px;
        --radius-input: 8px;
    }

    /* Global Theme Overrides */
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-body) !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.8 !important;
    }

    /* Remove heavy backgrounds */
    .background-orbs { display: none !important; }

    /* Layout & Whitespace */
    .main .block-container {
        padding-top: 4rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-heading) !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 1.5rem !important;
    }
    p, span, label, .stMarkdown {
        color: var(--text-body) !important;
        font-weight: 400 !important;
        line-height: 1.8 !important;
    }
    .stCaptionContainer p {
        color: var(--text-muted) !important;
        font-size: 0.9rem !important;
    }

    /* Containers -> Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg-surface) !important;
        border-radius: var(--radius-card) !important;
        border: none !important;
        box-shadow: var(--shadow-soft) !important;
        padding: 24px 32px !important;
        margin-bottom: 2rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
    }

    /* Actions: Buttons */
    .stButton button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-btn) !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: auto !important;
    }
    .stButton button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    .stButton button:active {
        transform: translateY(0px) !important;
    }

    /* Secondary/Ghost Buttons */
    .stButton button[kind="secondary"] {
        background: transparent !important;
        color: var(--text-body) !important;
        border: none !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: var(--border-light) !important;
        color: var(--text-heading) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Inputs */
    .stTextInput input, .stPasswordInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background: transparent !important;
        border: 1.5px solid var(--border-light) !important;
        border-radius: var(--radius-input) !important;
        padding: 0.75rem 1rem !important;
        color: var(--text-heading) !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput input:focus, .stPasswordInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }

    /* Data Display: Tables */
    [data-testid="stTable"] table {
        border: none !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }
    [data-testid="stTable"] th {
        background: transparent !important;
        color: var(--primary) !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        letter-spacing: 0.05em !important;
        border-bottom: 1px solid var(--border-light) !important;
        padding: 12px !important;
        text-align: left !important;
    }
    [data-testid="stTable"] td {
        border-bottom: 1px solid var(--border-light) !important;
        border-left: none !important;
        border-right: none !important;
        padding: 16px 12px !important;
        color: var(--text-body) !important;
    }

    /* Data Display: Lists */
    .stMarkdown ul {
        list-style: none !important;
        padding-left: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
    }
    .stMarkdown li {
        position: relative !important;
        padding-left: 24px !important;
    }
    .stMarkdown li::before {
        content: "•" !important;
        position: absolute !important;
        left: 0 !important;
        color: var(--primary) !important;
        font-weight: bold !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-surface) !important;
        border-right: 1px solid var(--border-light) !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: var(--bg-main) !important;
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: var(--border-light) !important;
        color: var(--primary) !important;
    }

    /* Hero & Landing Section Overrides */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(16, 185, 129, 0.1);
        color: var(--primary);
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: var(--text-heading);
        margin-bottom: 1.5rem;
        letter-spacing: -0.03em;
    }
    .gradient-text {
        background: linear-gradient(to right, var(--primary), #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: var(--text-body);
        margin-bottom: 2rem;
        max-width: 540px;
    }
    .glass-card {
        background: var(--bg-surface);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow-soft);
        padding: 2rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary);
    }
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        font-weight: 600;
    }
    .code-line {
        height: 8px;
        border-radius: 4px;
        background: var(--border-light);
        margin-bottom: 8px;
    }
    .code-line.highlight {
        background: var(--primary);
        opacity: 0.2;
    }
    
    .tha-search-link-btn {
        background: var(--bg-surface) !important;
        color: var(--primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        display: inline-block !important;
        transition: all 0.2s ease !important;
    }
    .tha-search-link-btn:hover {
        border-color: var(--primary) !important;
        background: var(--bg-main) !important;
    }

    </style>"""
    return saas_css
