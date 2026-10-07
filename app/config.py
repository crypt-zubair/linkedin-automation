from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
FACTS_FILE = DATA_DIR / "facts.json"
DB_FILE = DATA_DIR / "posts.db"
TOKEN_FILE = DATA_DIR / "token.json"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
ENABLE_AI_FACT_CHECK = os.getenv("ENABLE_AI_FACT_CHECK", "true").strip().lower() in {"1","true","yes","on"}
TEST_MODE = os.getenv("TEST_MODE", "true").strip().lower() in {"1","true","yes","on"}
MAX_POSTS = int(os.getenv("MAX_POSTS", "30"))
MIN_QUALITY_SCORE = float(os.getenv("MIN_QUALITY_SCORE", "7.5"))
GENERATION_RETRIES = int(os.getenv("GENERATION_RETRIES", "3"))

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()
LINKEDIN_REFRESH_TOKEN = os.getenv("LINKEDIN_REFRESH_TOKEN", "").strip()
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "").strip()
LINKEDIN_VERSION = os.getenv("LINKEDIN_VERSION", "202609").strip()
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://127.0.0.1:8765/callback").strip()
LINKEDIN_SCOPES = os.getenv("LINKEDIN_SCOPES", "w_member_social openid profile").strip()

for directory in (DATA_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)
