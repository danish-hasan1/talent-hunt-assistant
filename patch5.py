import sys

with open('app.py', 'r') as f:
    lines = f.readlines()

out_lines = []
in_style_block = False
style_block_lines = []

for i, line in enumerate(lines):
    if 'st.markdown("""' in line and '<style>' in lines[min(i+1, len(lines)-1)]:
        if lines[i-1].strip().startswith('if not st.session_state.get("user_email"):'):
            in_style_block = True
    
    if in_style_block:
        style_block_lines.append(line)
        if '        """, unsafe_allow_html=True)' in line:
            in_style_block = False
    else:
        out_lines.append(line)

# Dedent the style block
dedented_style = []
for line in style_block_lines:
    if line.startswith('    '):
        dedented_style.append(line[4:])
    else:
        dedented_style.append(line)

# Insert the style block before the 'if not st.session_state.get("user_email"):' line
for i, line in enumerate(out_lines):
    if line.strip().startswith('if not st.session_state.get("user_email"):'):
        target_idx = i
        break

final_lines = out_lines[:target_idx] + dedented_style + out_lines[target_idx:]

with open('app.py', 'w') as f:
    f.writelines(final_lines)
