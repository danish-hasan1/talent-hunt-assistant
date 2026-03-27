import sys

with open('search.py', 'r') as f:
    code = f.read()

# 1. Remove the old render logic from the boolean tab
old_block = """            links = st.session_state.get("search_links") or []
            if links:
                st.markdown("**Search links**")
                st.markdown(
                    \"\"\"
                    <style>
                    .tha-search-btn {
                        display:inline-block;
                        margin:0.2rem 0.4rem 0.2rem 0;
                        padding:0.25rem 0.8rem;
                        border-radius:999px;
                        border:1px solid #dee2e6;
                        background:#f8f9fa;
                        font-size:0.85rem;
                        text-decoration:none;
                        color:#212529;
                    }
                    .tha-search-btn:hover {
                        background:#e9ecef;
                    }
                    </style>
                    \"\"\",
                    unsafe_allow_html=True,
                )
                for item in links:
                    label = item.get("label", "Search")
                    url = item.get("url", "")
                    if not url:
                        continue
                    st.markdown(
                        f"<a class='tha-search-btn' href='{url}' target='_blank'>{label}</a>",
                        unsafe_allow_html=True,
                    )"""
code = code.replace(old_block, "")

# 2. Insert the new horizontal flexbox layout directly after line 641 or right before the RESULTS header summary.
# Look for:
#     if not results:
#         st.info(
#             "Search triggered. Use the search links below and the boolean strings to explore candidates in your browser. "
#             "Existing DB was also searched but no matches were found yet."
#         )
# 
# 
# # ===========================================================================
# # RESULTS

target = """    if not results:
        st.info(
            "Search triggered. Use the search links below and the boolean strings to explore candidates in your browser. "
            "Existing DB was also searched but no matches were found yet."
        )

"""
new_ui = """    if not results:
        st.info("Search triggered. Review the AI matches below or explore candidates instantly using the generated external pipeline links.")

links = st.session_state.get("search_links") or []
if links:
    st.markdown("<div style='display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1.5rem; justify-content: center;'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

"""
code = code.replace(target, new_ui)

with open('search.py', 'w') as f:
    f.write(code)
