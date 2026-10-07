from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from app.config import DB_FILE

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_id INTEGER NOT NULL UNIQUE,
    category TEXT NOT NULL,
    fact TEXT NOT NULL,
    source TEXT NOT NULL,
    post_text TEXT NOT NULL,
    quality_score REAL NOT NULL,
    status TEXT NOT NULL,
    linkedin_post_id TEXT,
    created_at TEXT NOT NULL
);
"""

def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_FILE)
    connection.execute(SCHEMA)
    connection.commit()
    return connection

def used_fact_ids(connection: sqlite3.Connection) -> set[int]:
    rows = connection.execute("SELECT fact_id FROM posts").fetchall()
    return {int(row[0]) for row in rows}

def completed_count(connection: sqlite3.Connection) -> int:
    row = connection.execute("SELECT COUNT(*) FROM posts WHERE status IN ('TEST_SAVED','PUBLISHED')").fetchone()
    return int(row[0])

def save_post(connection: sqlite3.Connection, *, fact_id: int, category: str, fact: str, source: str,
              post_text: str, quality_score: float, status: str, linkedin_post_id: str | None = None) -> None:
    connection.execute(
        """INSERT INTO posts
        (fact_id, category, fact, source, post_text, quality_score, status, linkedin_post_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (fact_id, category, fact, source, post_text, quality_score, status,
         linkedin_post_id, datetime.now(timezone.utc).isoformat()),
    )
    connection.commit()
