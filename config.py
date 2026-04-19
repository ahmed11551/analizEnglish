"""Настройки из окружения. Секреты только в .env (не коммитить)."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


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
