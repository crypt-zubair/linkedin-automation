from __future__ import annotations

import json
import requests

from app.config import ENABLE_AI_FACT_CHECK, OLLAMA_MODEL, OLLAMA_URL

FORBIDDEN = ("i'm excited to announce", "as an ai", "game-changing", "revolutionary", "10x")

def _basic_check(text: str) -> tuple[float, list[str]]:
    score = 10.0
    notes = []
    words = text.split()
    hashtags = [x for x in words if x.startswith("#")]
    if len(words) > 100:
        score -= 2.0
        notes.append("over 100 words")
    elif len(words) < 35:
        score -= 1.0
        notes.append("under 35 words")
    if len(hashtags) > 4:
        score -= 1.0
        notes.append("too many hashtags")
    lower = text.lower()
    for phrase in FORBIDDEN:
        if phrase in lower:
            score -= 2.0
            notes.append("discouraged phrase: " + phrase)
    if text.count("!") > 2:
        score -= 0.5
        notes.append("too many exclamation marks")
    if "http://" in lower or "https://" in lower:
        score -= 0.5
        notes.append("unexpected URL")
    return max(0.0, min(10.0, score)), notes

def _ai_fact_check(text: str, fact: dict) -> tuple[float, list[str]]:
    prompt = """Compare the candidate LinkedIn post with the supplied source fact.
The source fact is authoritative. Identify unsupported factual claims, changed numbers,
changed dates, invented details, or meaning changes. Ignore harmless wording differences.
Return ONLY JSON with this exact shape:
{"score": 0, "unsupported_claims": []}
Score from 0 to 10. A fully faithful paraphrase should score 9 or 10.
Any invented factual detail should reduce the score.
Source fact: {fact}
Candidate post: {post}
""".format(fact=fact["fact"], post=text)

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "options": {"temperature": 0.0},
        "messages": [
            {"role": "system", "content": "You are a strict factual consistency checker. Return JSON only."},
            {"role": "user", "content": prompt},
        ],
    }
    response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    response.raise_for_status()
    raw = response.json()["message"]["content"].strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("Fact checker did not return JSON.")
    result = json.loads(raw[start:end + 1])
    score = float(result["score"])
    unsupported = result.get("unsupported_claims", [])
    if not isinstance(unsupported, list):
        unsupported = [str(unsupported)]
    return max(0.0, min(10.0, score)), [str(x) for x in unsupported]

def check_post(text: str, fact: dict) -> tuple[float, list[str]]:
    basic_score, notes = _basic_check(text)
    if not ENABLE_AI_FACT_CHECK:
        return basic_score, notes

    try:
        fact_score, fact_notes = _ai_fact_check(text, fact)
        notes.extend(["AI fact check: " + x for x in fact_notes])
        return min(basic_score, fact_score), notes
    except Exception as exc:
        # Fail closed: do not publish a post when the factual safety check cannot run.
        notes.append("AI fact check failed: " + str(exc))
        return 0.0, notes
