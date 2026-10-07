from __future__ import annotations
import logging
from app.config import LOG_DIR

LOG_FILE = LOG_DIR / "autopilot.log"

def get_logger() -> logging.Logger:
    logger = logging.getLogger("linkedin_autopilot")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger
