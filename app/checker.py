from __future__ import annotations

FORBIDDEN = ('i\'m excited to announce', 'as an ai', 'game-changing', 'revolutionary', '10x')

def check_post(text: str, fact: dict) -> tuple[float, list[str]]:
    score = 10.0
    notes = []
    words = text.split()
    hashtags = [x for x in words if x.startswith('#')]
    if len(words) > 100:
        score -= 2.0
        notes.append('over 100 words')
    elif len(words) < 35:
        score -= 1.0
        notes.append('under 35 words')
    if len(hashtags) > 4:
        score -= 1.0
        notes.append('too many hashtags')
    lower = text.lower()
    for phrase in FORBIDDEN:
        if phrase in lower:
            score -= 2.0
            notes.append('discouraged phrase: ' + phrase)
    if text.count('!') > 2:
        score -= 0.5
        notes.append('too many exclamation marks')
    if 'http://' in lower or 'https://' in lower:
        score -= 0.5
        notes.append('unexpected URL')
    return max(0.0, min(10.0, score)), notes
