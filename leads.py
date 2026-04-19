"""Запись лидов (контакт после теста) в JSON Lines."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import LEADS_PATH

_CONTACT_STORE_MAX = 500


def append_lead(record: dict[str, Any]) -> None:
    path: Path = LEADS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    c = record.get("contact")
    if isinstance(c, str) and len(c) > _CONTACT_STORE_MAX:
        record = {**record, "contact": c[:_CONTACT_STORE_MAX] + "…"}
    line = json.dumps(record, ensure_ascii=False, default=str)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def build_lead_record(
    *,
    user_id: int | None,
    username: str | None,
    first_name: str | None,
    contact: str | None,
    skipped: bool,
    intro: dict[str, str],
    score: int,
    level_label: str,
    wrong_topics: list[str],
) -> dict[str, Any]:
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "contact": contact,
        "skipped": skipped,
        "intro": intro,
        "score": score,
        "level": level_label,
        "wrong_topics": wrong_topics,
    }
