import sys

def patch_theme_py():
    with open('theme.py', 'r') as f:
        code = f.read()

    # We will inject the new CSS block right before the closing </style> tag in get_theme_css
    target_pos = code.find('</style>')
    if target_pos == -1:
        print("Could not find </style> in theme.py")
        return

    # Phase 6: Sidebar CSS
    sidebar_css = """
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
    """
    
    # Inject it right before </style>
    new_code = code[:target_pos] + sidebar_css + code[target_pos:]
    
    with open('theme.py', 'w') as f:
        f.write(new_code)
        
if __name__ == "__main__":
    patch_theme_py()
    print("Patched theme.py")
