from __future__ import annotations
import random
import requests
from app.config import GENERATION_RETRIES, OLLAMA_MODEL, OLLAMA_URL

STYLES = (
    'surprise: open with a surprising direct statement, then explain it.',
    'question: open with a short curiosity question, then answer it.',
    'comparison: compare two familiar ideas to make the fact easy to understand.',
    'story: use a compact observation that feels natural and human.',
)

SYSTEM_PROMPT = '''You write short LinkedIn technology posts for an engineering student.
The supplied fact is the ONLY factual authority.
Never invent, exaggerate, speculate, add numbers, dates, or unsupported claims.
Use 35-100 words, one fact, natural language, an interesting opening, and 2-4 relevant hashtags.
No fake personal experiences, corporate buzzwords, or I'm excited to announce.
Do not say you are an AI. Avoid excessive emojis. Return ONLY the final post.'''

def generate_post(fact: dict) -> tuple[str, str]:
    style = random.choice(STYLES)
    prompt = 'Source fact:\nCategory: {}\nFact: {}\n\nStyle: {}\nWrite the final LinkedIn post.'.format(fact['category'], fact['fact'], style)
    payload = {'model': OLLAMA_MODEL, 'stream': False, 'options': {'temperature': 0.75, 'top_p': 0.9},
               'messages': [{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': prompt}]}
    last_error = None
    for _ in range(GENERATION_RETRIES):
        try:
            response = requests.post(f'{OLLAMA_URL}/api/chat', json=payload, timeout=120)
            response.raise_for_status()
            text = response.json()['message']['content'].strip().strip('`').strip()
            if not text:
                raise ValueError('Ollama returned an empty post.')
            return text, style
        except (requests.RequestException, KeyError, ValueError) as exc:
            last_error = exc
    raise RuntimeError(f'Post generation failed: {last_error}')
