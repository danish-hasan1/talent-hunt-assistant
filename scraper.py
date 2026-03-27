from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from db import upsert_candidate, link_candidate_to_job, get_job_candidates
from boolean_builder import generate_all_strings


JOB_BOARD_SITES: List[str] = [
    # India
    "naukri.com",
    "foundit.in",
    "instahyre.com",
    # US / global
    "ziprecruiter.com",
    "glassdoor.com",
    "wellfound.com",
    # UK
    "reed.co.uk",
    "totaljobs.com",
    "cv-library.co.uk",
    # Spain / Italy
    "infojobs.net",
    "infoempleo.com",
    "tecnoempleo.com",
    # Germany
    "stepstone.de",
    "xing.com",
    # France
    "apec.fr",
    "pole-emploi.fr",
    "wttj.co",
    # Netherlands
    "werk.nl",
    "nationalevacaturebank.nl",
    # Sweden
    "arbetsformedlingen.se",
    "blocketjobb.se",
    # Middle East
    "bayt.com",
    "naukrigulf.com",
    "gulftalent.com",
    # Singapore
    "mycareersfuture.gov.sg",
    "jobscentral.com.sg",
    # Australia
    "seek.com.au",
    "jora.com",
    # Canada
    "workopolis.com",
    "jobbank.gc.ca",
    # Japan
    "rikunabi.com",
    "daijob.com",
    # China
    "zhaopin.com",
    "51job.com",
    "liepin.com",
]


def fetch_jd_text(url: str) -> str:
    return f"Job description placeholder fetched from {url}"


def run_scrapers_for_job(job_id: Optional[int], filter_config: Dict[str, Any]) -> List[str]:
    boolean_strings = generate_all_strings(filter_config)
    sources = filter_config.get("sources", {}) or {}

    search_urls: List[str] = []

    # LinkedIn X-ray searches (Google)
    if sources.get("linkedin", True):
        broad_query = boolean_strings.get("linkedin_broad") or ""
        balanced_query = boolean_strings.get("linkedin_balanced") or ""

        titles = filter_config.get("titles", [])
        title_terms = [f'"{t.strip()}"' for t in titles if t and t.strip()]
        minimal_query = ""
        if title_terms:
            minimal_query = "site:linkedin.com/in " + "(" + " OR ".join(title_terms[:4]) + ")"

        if broad_query:
            search_urls.append("https://www.google.com/search?q=" + quote_plus(broad_query))
        elif balanced_query:
            search_urls.append("https://www.google.com/search?q=" + quote_plus(balanced_query))

        if minimal_query and minimal_query not in (broad_query, balanced_query):
            search_urls.append("https://www.google.com/search?q=" + quote_plus(minimal_query))

    # GitHub profiles via Google X-ray
    if sources.get("github"):
        github_q = boolean_strings.get("github") or ""
        if github_q:
            search_urls.append("https://www.google.com/search?q=" + quote_plus(github_q))

    # General Google search without site restriction (for blogs, portfolios, etc.)
    if sources.get("google"):
        core_q = boolean_strings.get("linkedin_balanced") or ""
        if core_q.startswith("site:linkedin.com/in "):
            core_q = core_q.replace("site:linkedin.com/in ", "", 1).strip()
        if core_q:
            people_q = (
                core_q
                + ' "profile" OR "resume" OR "cv"'
                + ' -"jobs" -job -hiring -careers -vacancy -apply -recruiting'
            )
            search_urls.append("https://www.google.com/search?q=" + quote_plus(people_q))

    # Global job board style search via Google X-ray using public, indexable pages only
    if sources.get("naukri"):
        params = boolean_strings.get("naukri_params") or {}
        keywords = params.get("keywords") or ""
        skills = params.get("skills") or ""
        location = params.get("location") or ""
        site_clause = " OR ".join(f"site:{s}" for s in JOB_BOARD_SITES)
        parts = [f"({site_clause})"]
        for val in (keywords, skills, location):
            if val:
                parts.append(f'"{val}"')
        # Bias towards candidate pages / resumes, away from job ads
        parts.append('"profile" OR "resume" OR "cv"')
        parts.append('-"jobs" -job -hiring -careers -vacancy')
        naukri_q = " ".join(parts)
        if naukri_q:
            search_urls.append("https://www.google.com/search?q=" + quote_plus(naukri_q))

    return search_urls
