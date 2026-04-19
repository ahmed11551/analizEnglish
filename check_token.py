"""Exit 0 if BOT_TOKEN in .env looks set, else 1. Used by run_bot.ps1."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
t = (os.environ.get("BOT_TOKEN") or "").strip()
sys.exit(0 if len(t) > 20 else 1)
