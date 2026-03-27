import json
from typing import Any, Dict, Tuple

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMP, GROQ_MAX_TOKENS
from jd_analysis import _parse_json


def _get_client() -> Groq:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")
    return Groq(api_key=GROQ_API_KEY)


def score_candidate_for_job(filter_config: Dict[str, Any], candidate: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    try:
        client = _get_client()
    except ValueError:
        return 0.0, {}

    system = (
        "You are an expert hiring assessor. Given structured job filter parameters and a candidate profile, "
        "assign a match score from 0 to 100 and explain the breakdown. A score of 80+ means strong fit, "
        "60-79 is workable with gaps, below 60 is weak fit."
    )

    payload = {
        "filter_config": filter_config,
        "candidate": {
            "full_name": candidate.get("full_name"),
            "current_title": candidate.get("current_title"),
            "current_company": candidate.get("current_company"),
            "location": candidate.get("location"),
            "skills": candidate.get("skills", []),
            "experience_years": candidate.get("experience_years"),
        },
    }

    user_message = (
        "Evaluate how well this candidate matches the role described by the filter_config. "
        "Focus on titles, skills, location and years of experience.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}\n\n"
        "Return valid JSON with this exact structure:\n"
        "{\n"
        '  "match_score": number,\n'
        '  "score_breakdown": {\n'
        '    "skills": number,\n'
        '    "experience": number,\n'
        '    "location": number,\n'
        '    "seniority": number,\n'
        '    "notes": "string"\n'
        "  }\n"
        "}"
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=GROQ_TEMP,
        max_tokens=GROQ_MAX_TOKENS,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content.strip()
    try:
        parsed = _parse_json(raw)
    except Exception:
        return 0.0, {}

    score = float(parsed.get("match_score", 0.0))
    if score < 0:
        score = 0.0
    if score > 100:
        score = 100.0
    breakdown = parsed.get("score_breakdown") or {}
    return score, breakdown

