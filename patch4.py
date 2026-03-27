import sys

with open('app.py', 'r') as f:
    text = f.read()

new_internal_css = """
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
"""

text = text.replace("        </style>", new_internal_css + "\n        </style>")

with open('app.py', 'w') as f:
    f.write(text)
