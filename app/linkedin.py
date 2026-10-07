from __future__ import annotations
import requests
from app.config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN, LINKEDIN_VERSION

API_URL = 'https://api.linkedin.com/rest/posts'

def publish_post(text: str) -> str:
    if not LINKEDIN_ACCESS_TOKEN:
        raise RuntimeError('LINKEDIN_ACCESS_TOKEN is not configured.')
    if not LINKEDIN_PERSON_URN:
        raise RuntimeError('LINKEDIN_PERSON_URN is not configured.')
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
        'Linkedin-Version': LINKEDIN_VERSION,
    }
    payload = {
        'author': LINKEDIN_PERSON_URN,
        'commentary': text,
        'visibility': 'PUBLIC',
        'distribution': {'feedDistribution': 'MAIN_FEED', 'targetEntities': [], 'thirdPartyDistributionChannels': []},
        'lifecycleState': 'PUBLISHED',
        'isReshareDisabledByAuthor': False,
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    if response.status_code >= 400:
        try: details = response.json()
        except ValueError: details = response.text
        raise RuntimeError(f'LinkedIn API returned HTTP {response.status_code}: {details}')
    post_id = response.headers.get('x-restli-id')
    if post_id: return post_id
    try: return str(response.json()['id'])
    except (ValueError, KeyError): raise RuntimeError('LinkedIn returned no post ID.')
