import sys

with open('search.py', 'r') as f:
    code = f.read()

target = """    st.markdown("<div style='display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem; justify-content: center;'>", unsafe_allow_html=True)
    for item in links:
        label = item.get("label", "Search")
        url = item.get("url", "")
        if url:
            icon = "↗"
            if "LinkedIn" in label: icon = "💼"
            elif "GitHub" in label: icon = "💻"
            elif "Google" in label: icon = "🔍"
            st.markdown(
                f"<a class='tha-search-link-btn' href='{url}' target='_blank'>{icon} {label}</a>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)"""

new_code = """    html_str = "<div style='display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem; justify-content: center;'>"
    for item in links:
        label = item.get("label", "Search")
        url = item.get("url", "")
        if url:
            icon = "↗"
            if "LinkedIn" in label: icon = "💼"
            elif "GitHub" in label: icon = "💻"
            elif "Google" in label: icon = "🔍"
            html_str += f"<a class='tha-search-link-btn' href='{url}' target='_blank'>{icon} {label}</a>"
    html_str += "</div>"
    st.markdown(html_str, unsafe_allow_html=True)"""

if target in code:
    code = code.replace(target, new_code)
    with open('search.py', 'w') as f:
        f.write(code)
    print("Success")
else:
    print("Target not found")
