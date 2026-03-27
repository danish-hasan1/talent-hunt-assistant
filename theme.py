def get_theme_css(theme: str) -> str:
    dark_css = r"""<style>
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


    /* Internal Widget Overrides */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #F8FAFC !important;
    }
    
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(255, 255, 255, 0.15) !important;
    }
    [data-testid="stExpander"] summary {
        background: transparent !important;
        padding: 0.75rem 1rem !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #38BDF8 !important;
    }
    [data-testid="stExpander"] summary svg {
        fill: #94A3B8 !important;
    }
    [data-testid="stExpander"] p {
        color: #cbd5e1 !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stNumberInput input {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }
    
    [data-baseweb="popover"] > div {
        background: #0B0F19 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="menu"] li {
        color: #F8FAFC !important;
    }
    [data-baseweb="menu"] li:hover {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #38BDF8 !important;
    }

    [data-testid="stAlert"] {
        background: rgba(11, 15, 25, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        color: #F8FAFC !important;
    }
    /* Color border overlays for alerts */
    [data-testid="stAlert"]:has([aria-label="Warning"]) { border-left: 4px solid #F59E0B !important; background: rgba(245, 158, 11, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Info"]) { border-left: 4px solid #3B82F6 !important; background: rgba(59, 130, 246, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Success"]) { border-left: 4px solid #10B981 !important; background: rgba(16, 185, 129, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Error"]) { border-left: 4px solid #EF4444 !important; background: rgba(239, 68, 68, 0.05) !important; }

    [data-testid="stCheckbox"] {
        color: #94A3B8 !important;
    }
    [data-testid="stCheckbox"] > label > div[data-baseweb="checkbox"] > div {
        background-color: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
    }

    [data-baseweb="tag"] {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    .tha-search-link-btn {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.25rem;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.05);
        color: #F8FAFC !important;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.15);
        text-decoration: none !important;
        transition: all 0.3s ease;
    }
    .tha-search-link-btn:hover {
        transform: translateY(-2px);
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.4);
        color: #38BDF8 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
    }


        /* Text Legibility Overrides */
        .stMarkdown p, label, .stWidgetLabel, .stWidgetLabel p, .stWidgetLabel span, 
        .stCheckbox span, [data-testid="stMarkdownContainer"] p, [data-testid="stText"] { 
            color: #F8FAFC !important; 
        }

    
    /* --- Phase 6: Sidebar Navigation Overhaul --- */
    /* Target the radio group explicitly in the sidebar */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    /* Style the label as a full-width glass pill */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        padding: 0.75rem 1rem !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        width: 100%;
        margin-bottom: 0 !important;
        display: flex;
        align-items: center;
    }
    
    /* Hide the native circular radio input geometry */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-of-type {
        display: none !important;
    }
    
    /* Override text styling inside the pill */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        color: #94A3B8 !important;
        margin: 0 !important;
        transition: color 0.3s ease !important;
    }
    
    /* Hover effects */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover p {
        color: #F8FAFC !important;
    }

    /* Active (Checked) state styling */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(129, 140, 248, 0.15) !important;
        border-color: #818CF8 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* --- Note: Ensure light theme overrides this appropriately below in get_theme_css --- */
    </style>"""
    
    light_css = r"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global Theme Override for Streamlit */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
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
        color: #0F172A;
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
        color: #475569; 
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
        background: rgba(0, 0, 0, 0.03); 
        color: #818CF8;
        font-size: 0.85rem; 
        font-weight: 600;
        border: 1px solid rgba(0, 0, 0, 0.1);
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
        color: #0F172A;
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
        color: #38BDF8;
        font-weight: bold;
    }
    
    /* Streamlit native container override */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        background: rgba(0, 0, 0, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: all 0.4s ease;
        overflow: hidden;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.6) !important;
        transform: translateY(-3px);
        border-color: rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Native Streamlit Text Inputs */
    .stTextInput input, .stPasswordInput input {
        background: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #0F172A !important;
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
        color: #475569 !important;
        font-weight: 600;
        background: transparent !important;
        border-bottom-width: 2px !important;
        padding-bottom: 0.5rem !important;
        border-bottom-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        border-bottom-color: #4F46E5 !important;
    }
    
    /* Typography overrides for internal markdown */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #0F172A !important;
    }
    .stMarkdown .stCaptionContainer p {
        color: #475569 !important;
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
        color: #0F172A !important;
        letter-spacing: -0.01em;
    }
    .tha-feature-text { 
        color: #475569; 
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
        color: #475569;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    .tha-hiw-content strong {
        color: #0F172A;
    }

    /* Raw Vite Structural Elements */
    .badge { display: inline-block; padding: 0.4rem 1rem; border-radius: 9999px; background: rgba(56, 189, 248, 0.1); color: #38BDF8; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(56, 189, 248, 0.2); margin-bottom: 2rem; }
    .hero-title { font-size: 4rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; color: #0F172A !important; margin-bottom: 1.5rem; }
    .hero-title br { display: block; }
    .gradient-text { background: linear-gradient(to right, #38BDF8, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-size: 200% auto; animation: shine 4s linear infinite; }
    .hero-subtitle { font-size: 1.25rem; color: #475569 !important; font-weight: 300; max-width: 580px; line-height: 1.6; margin-bottom: 3rem; }
    
    .hero-visual-wrapper { position: relative; display: flex; justify-content: flex-start; align-items: center; margin-top: 2rem; min-height: 350px; }
    .glass-card { background: rgba(0, 0, 0, 0.03); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 20px; padding: 2rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05); }
    .preview-card { width: 100%; max-width: 350px; height: 280px; display: flex; flex-direction: column; gap: 1rem; transform: rotate(5deg) scale(1.05); animation: floatCard 6s infinite ease-in-out; margin-left: 2rem; }
    @keyframes floatCard { 0%, 100% { transform: rotate(5deg) translateY(0); } 50% { transform: rotate(4deg) translateY(-20px); } }
    .stat-card { position: absolute; top: -10%; left: 0%; padding: 1.5rem; z-index: 2; transform: rotate(-5deg); animation: floatStat 7s infinite ease-in-out; }
    @keyframes floatStat { 0%, 100% { transform: rotate(-5deg) translateY(0); } 50% { transform: rotate(-3deg) translateY(15px); } }
    .stat-number { font-size: 2.5rem; font-weight: 800; color: #38BDF8; line-height: 1; }
    .stat-label { font-size: 0.85rem; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem; }
    .code-line { height: 12px; border-radius: 6px; background: rgba(0, 0, 0, 0.1); }
    .w-80 { width: 80%; } .w-60 { width: 60%; } .w-40 { width: 40%; } .w-90 { width: 90%; } .w-70 { width: 70%; }
    .highlight { background: linear-gradient(90deg, #4F46E5, #C084FC); }
    
    .features-header { text-align: center; margin-bottom: 4rem; margin-top: 4rem; }
    .features-header h2 { font-size: 3rem; font-weight: 800; letter-spacing: -0.02em; color: #0F172A !important; }
    .gradient-text-alt { background: linear-gradient(to right, #C084FC, #F472B6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; margin-bottom: 4rem; }
    .feature-card { padding: 3rem 2rem; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; background: rgba(0, 0, 0, 0.03); backdrop-filter: blur(12px); border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 20px;}
    .feature-card:hover { transform: translateY(-8px); border-color: rgba(255, 255, 255, 0.2); background: rgba(255, 255, 255, 0.05); }
    .feature-icon.bg-purple { background: rgba(192, 132, 252, 0.15); color: #C084FC; border: 1px solid rgba(192, 132, 252, 0.3); }
    .feature-icon.bg-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .feature-icon.bg-emerald { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .feature-card h3 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: #0F172A !important;}
    .feature-card p { color: #475569; font-size: 1.05rem; }


    /* Internal Widget Overrides */
    [data-testid="stSidebar"] {
        background-color: rgba(248, 250, 252, 0.95) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #0F172A !important;
    }
    
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(0, 0, 0, 0.15) !important;
    }
    [data-testid="stExpander"] summary {
        background: transparent !important;
        padding: 0.75rem 1rem !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #38BDF8 !important;
    }
    [data-testid="stExpander"] summary svg {
        fill: #475569 !important;
    }
    [data-testid="stExpander"] p {
        color: #334155 !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stNumberInput input {
        background: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }
    
    [data-baseweb="popover"] > div {
        background: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="menu"] li {
        color: #0F172A !important;
    }
    [data-baseweb="menu"] li:hover {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #38BDF8 !important;
    }

    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
        color: #0F172A !important;
    }
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        color: #0F172A !important;
    }
    /* Color border overlays for alerts */
    [data-testid="stAlert"]:has([aria-label="Warning"]) { border-left: 4px solid #F59E0B !important; background: rgba(245, 158, 11, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Info"]) { border-left: 4px solid #3B82F6 !important; background: rgba(59, 130, 246, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Success"]) { border-left: 4px solid #10B981 !important; background: rgba(16, 185, 129, 0.05) !important; }
    [data-testid="stAlert"]:has([aria-label="Error"]) { border-left: 4px solid #EF4444 !important; background: rgba(239, 68, 68, 0.05) !important; }

    [data-testid="stCheckbox"] {
        color: #475569 !important;
    }
    [data-testid="stCheckbox"] > label > div[data-baseweb="checkbox"] > div {
        background-color: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
    }

    [data-baseweb="tag"] {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    .tha-search-link-btn {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.25rem;
        border-radius: 9999px;
        background: rgba(0, 0, 0, 0.03);
        color: #0F172A !important;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid rgba(0, 0, 0, 0.1);
        text-decoration: none !important;
        transition: all 0.3s ease;
    }
    .tha-search-link-btn:hover {
        transform: translateY(-2px);
        background: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.4);
        color: #0284C7 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
    }


        /* Text Legibility Overrides */
        .stMarkdown p, label { color: #0F172A !important; }

    </style>"""
    
    return dark_css if theme == "dark" else light_css
