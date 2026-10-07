from __future__ import annotations
import json, random
from app.config import FACTS_FILE
from app.database import used_fact_ids

def load_facts() -> list[dict]:
    facts = json.loads(FACTS_FILE.read_text(encoding="utf-8"))
    if not isinstance(facts, list) or not facts:
        raise ValueError("facts.json must contain a non-empty list.")
    required = {"id","category","fact","source"}
    if any(not required.issubset(x) for x in facts):
        raise ValueError("Every fact needs id, category, fact and source.")
    ids = [int(x["id"]) for x in facts]
    if len(ids) != len(set(ids)):
        raise ValueError("Fact IDs must be unique.")
    return facts

def select_unused_fact(connection) -> dict:
    facts = load_facts()
    used = used_fact_ids(connection)
    available = [x for x in facts if int(x["id"]) not in used]
    if not available:
        raise RuntimeError("No unused facts remain.")
    return random.SystemRandom().choice(available)
