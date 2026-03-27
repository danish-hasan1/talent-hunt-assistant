from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus
import webbrowser

from db import upsert_candidate, link_candidate_to_job, get_job_candidates
from boolean_builder import generate_all_strings


def fetch_jd_text(url: str) -> str:
    return f"Job description placeholder fetched from {url}"


def run_scrapers_for_job(job_id: Optional[int], filter_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    boolean_strings = generate_all_strings(filter_config)
    broad_query = boolean_strings.get("linkedin_broad") or ""
    balanced_query = boolean_strings.get("linkedin_balanced") or ""

    titles = filter_config.get("titles", [])
    title_terms = [f'"{t.strip()}"' for t in titles if t and t.strip()]
    minimal_query = ""
    if title_terms:
        minimal_query = "site:linkedin.com/in " + "(" + " OR ".join(title_terms[:4]) + ")"

    search_urls: List[str] = []
    if broad_query:
        search_urls.append("https://www.google.com/search?q=" + quote_plus(broad_query))
    elif balanced_query:
        search_urls.append("https://www.google.com/search?q=" + quote_plus(balanced_query))

    if minimal_query and minimal_query not in (broad_query, balanced_query):
        search_urls.append("https://www.google.com/search?q=" + quote_plus(minimal_query))

    for url in search_urls:
        try:
            webbrowser.open_new_tab(url)
        except Exception:
            continue

    return []
