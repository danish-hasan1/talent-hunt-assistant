import sys

# Read original
with open('app.py', 'r') as f:
    text = f.read()

# 1. Add CSS before </style>
new_css = """
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
"""
text = text.replace("        </style>", new_css + "\n        </style>")

# 2. Replace the hero_left content (Lines 305 to 335)
old_hero_left = """            st.markdown("<div class='tha-hero-title'>Talent Hunt Assistant</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='tha-hero-subtitle'>Turn messy job descriptions into structured searches, reusable pipelines, and AI‑scored shortlists without handing everything to a third‑party ATS.</div>",
                unsafe_allow_html=True,
            )
            
            st.markdown("<div class='tha-list-title'>Built for senior recruiters and sourcing leads who:</div>", unsafe_allow_html=True)
            st.markdown(
                \"\"\"
                <ul class='tha-list'>
                    <li>Want JD-driven, repeatable search setups instead of ad‑hoc strings.</li>
                    <li>Run multi‑region searches and need a single workspace to track them.</li>
                    <li>Prefer owning their own candidate database rather than renting access.</li>
                </ul>
                \"\"\",
                unsafe_allow_html=True
            )
            
            st.markdown("<div class='tha-list-title' style='margin-top:2.5rem;'>Signals you control</div>", unsafe_allow_html=True)
            st.markdown(
                \"\"\"
                <div class='tha-pills-container'>
                    <span class='tha-pill'>🎯 JD‑driven filters</span>
                    <span class='tha-pill'>🌐 Multi‑source X‑ray</span>
                    <span class='tha-pill'>🤖 AI scoring</span>
                    <span class='tha-pill'>📊 Per‑job pipeline</span>
                </div>
                \"\"\",
                unsafe_allow_html=True,
            )"""

new_hero_left = """            st.markdown(\"\"\"
            <div class="badge">Version 2.0 Live ✨</div>
            <div class="hero-title">
                Intelligent <br/>
                <span class="gradient-text">Talent Sourcing</span>
            </div>
            <div class="hero-subtitle">
                Turn messy job descriptions into structured searches, reusable pipelines, and AI‑scored shortlists without handing everything to a third‑party ATS.
            </div>
            <div class="hero-visual-wrapper">
                <div class="glass-card stat-card">
                    <div class="stat-number">4x</div>
                    <div class="stat-label">Faster Sourcing</div>
                </div>
                <div class="glass-card preview-card">
                    <div class="code-line w-80"></div>
                    <div class="code-line w-60"></div>
                    <div class="code-line w-40 highlight"></div>
                    <div class="code-line w-90"></div>
                    <div class="code-line w-70"></div>
                </div>
            </div>
            \"\"\", unsafe_allow_html=True)"""
text = text.replace(old_hero_left, new_hero_left)


# 3. Replace the 3 features columns with raw HTML Grid
# From `feat_col1, feat_col2, feat_col3 = st.columns(3)` up to the `st.markdown("</div>", unsafe_allow_html=True)`
old_features_block = """        feat_col1, feat_col2, feat_col3 = st.columns(3)
        with feat_col1:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>⚡</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Analyse any JD</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Break job descriptions into titles, skills, seniority and non‑negotiables with one click, then tweak filters like you would in a world‑class RPS.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        with feat_col2:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>🌍</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Source everywhere</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Generate X‑ray searches for LinkedIn, GitHub, Google and major regional job boards so you can directly target candidates where they actually are.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        with feat_col3:
            with st.container(border=True):
                st.markdown("<div style='padding: 1rem 0.5rem;'>", unsafe_allow_html=True)
                st.markdown("<div class='tha-feature-icon'>🏦</div>", unsafe_allow_html=True)
                st.markdown("<div class='tha-section-title'>Own your DB</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='tha-feature-text'>Save candidates once, attach them to multiple roles, track stages and match scores, and keep everything inside a unified database you control.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)"""

new_features_block = """        st.markdown(\"\"\"
        <div class="features-header">
            <h2>Everything you need, <span class="gradient-text-alt">nothing you don't.</span></h2>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="tha-feature-icon bg-purple">⚡</div>
                <h3>Analyse any JD</h3>
                <p>Break job descriptions into titles, skills, seniority and non‑negotiables with one click, then tweak filters like you would in a world‑class RPS.</p>
            </div>
            <div class="feature-card">
                <div class="tha-feature-icon bg-blue">🌍</div>
                <h3>Source everywhere</h3>
                <p>Generate X‑ray searches for LinkedIn, GitHub, Google and major regional job boards so you can directly target candidates where they actually are.</p>
            </div>
            <div class="feature-card">
                <div class="tha-feature-icon bg-emerald">🏦</div>
                <h3>Own your DB</h3>
                <p>Save candidates once, attach them to multiple roles, track stages and match scores, and keep everything inside a unified database you control.</p>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)"""
text = text.replace(old_features_block, new_features_block)


# Remove `hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])` duplication
text = text.replace("hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])\n        hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])", "hero_left, hero_spacer, hero_right = st.columns([1.1, 0.1, 0.9])")

with open('app.py', 'w') as f:
    f.write(text)
