import sys

with open("app.py", "r") as f:
    lines = f.readlines()

out_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith('if not st.session_state.get("user_email"):'):
        skip = True
        out_lines.append(line)
        out_lines.append('''    st.markdown("""
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
''')
        continue
    if skip:
        if "hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])" in line:
            skip = False
            out_lines.append(line)
    if not skip:
        out_lines.append(line)

with open("app.py", "w") as f:
    f.writelines(out_lines)
