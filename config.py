"""Настройки из окружения. Секреты только в .env (не коммитить)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent

# Явный путь к .env рядом с проектом (не зависит от текущей папки в консоли)
_ENV_PATH = _ROOT / ".env"
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

# Куда писать лиды (JSON Lines). Каталог создаётся автоматически.
_leads_override = _env("LEADS_FILE")
LEADS_PATH = Path(_leads_override) if _leads_override else _ROOT / "data" / "leads.jsonl"

# HTTP(S) или SOCKS5 прокси для запросов к Telegram (если прямой доступ режется).
# Примеры: http://127.0.0.1:7890  socks5://127.0.0.1:1080
# Для socks5: pip install "python-telegram-bot[socks]"
TELEGRAM_PROXY = _env("TELEGRAM_PROXY")

# Публичные ссылки для CTA и mini app.
WEBSITE_URL = _env("WEBSITE_URL", "https://desharschool.ru")
MINI_APP_URL = _env("MINI_APP_URL", "")
