import sys

with open('app.py', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'st.markdown("""' in line.strip():
        if i+1 < len(lines) and '<style>' in lines[i+1].strip():
            start_idx = i
    if '""", unsafe_allow_html=True)' in line.strip() and start_idx != -1:
        end_idx = i
        break

if start_idx == -1 or end_idx == -1:
    print("Could not find the CSS block in app.py!")
    sys.exit(1)

dark_css = "".join(lines[start_idx+2:end_idx-1])

light_css = dark_css.replace('#0B0F19 !important', '#F8FAFC !important')
light_css = light_css.replace('#F8FAFC', '#0F172A')
light_css = light_css.replace('#94A3B8', '#475569')
light_css = light_css.replace('rgba(255, 255, 255, 0.03)', 'rgba(0, 0, 0, 0.03)')
light_css = light_css.replace('rgba(255, 255, 255, 0.08)', 'rgba(0, 0, 0, 0.08)')
light_css = light_css.replace('rgba(255, 255, 255, 0.1)', 'rgba(0, 0, 0, 0.1)')
light_css = light_css.replace('rgba(255, 255, 255, 0.15)', 'rgba(0, 0, 0, 0.15)')
light_css = light_css.replace('rgba(11, 15, 25, 0.95) !important', 'rgba(248, 250, 252, 0.95) !important')
light_css = light_css.replace('rgba(11, 15, 25, 0.8) !important', 'rgba(255, 255, 255, 0.9) !important')
light_css = light_css.replace('rgba(0, 0, 0, 0.5)', 'rgba(0, 0, 0, 0.05)')
light_css = light_css.replace('rgba(0, 0, 0, 0.2) !important', '#FFFFFF !important')
light_css = light_css.replace('color: #cbd5e1 !important', 'color: #334155 !important')
light_css = light_css.replace('color: #F8FAFC !important', 'color: #0F172A !important')

dark_css += "\n        /* Text Legibility Overrides */\n        .stMarkdown p, label { color: #E2E8F0 !important; }\n"
light_css += "\n        /* Text Legibility Overrides */\n        .stMarkdown p, label { color: #0F172A !important; }\n"

theme_py_content = f'''def get_theme_css(theme: str) -> str:
    dark_css = r\"\"\"<style>
{dark_css}
    </style>\"\"\"
    
    light_css = r\"\"\"<style>
{light_css}
    </style>\"\"\"
    
    return dark_css if theme == "dark" else light_css
'''

with open('theme.py', 'w') as f:
    f.write(theme_py_content)

new_injection = '''
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

from theme import get_theme_css
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)
'''

final_app_py = lines[:start_idx] + [new_injection] + lines[end_idx+1:]

with open('app.py', 'w') as f:
    f.writelines(final_app_py)
