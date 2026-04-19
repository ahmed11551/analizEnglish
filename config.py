"""Настройки из окружения. Секреты только в .env (не коммитить)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Явный путь к .env рядом с проектом (не зависит от текущей папки в консоли)
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)


def _env(name: str, default: str = "") -> str:
    v = os.environ.get(name)
    return (v or default).strip()


BOT_TOKEN = _env("BOT_TOKEN")

# Отображаемое имя продукта (как в BotFather / подпись к /start)
BRAND_TITLE = _env("BRAND_TITLE", "Тест английского · Grammar Check")
BRAND_SUBTITLE = _env(
    "BRAND_SUBTITLE",
    "Grammar & Usage (B2) · определение уровня и темы для повторения",
)

LOG_LEVEL = _env("LOG_LEVEL", "INFO").upper()
