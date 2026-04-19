"""
Показать у Telegram текущий webhook (URL, ошибки доставки, очередь).
Нужен BOT_TOKEN в .env или в окружении.

  python get_webhook_info.py
"""

from __future__ import annotations

import json
import sys
import urllib.request

from config import BOT_TOKEN


def main() -> None:
    if not BOT_TOKEN:
        print("Нет BOT_TOKEN", file=sys.stderr)
        sys.exit(1)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    try:
        raw = urllib.request.urlopen(url, timeout=30).read()
    except Exception as e:
        print("Сеть:", e, file=sys.stderr)
        sys.exit(1)
    out = json.loads(raw.decode("utf-8"))
    if not out.get("ok"):
        print("Telegram:", out, file=sys.stderr)
        sys.exit(1)
    info = out.get("result") or {}
    print(json.dumps(info, ensure_ascii=False, indent=2))
    err = (info.get("last_error_message") or "").strip()
    if err:
        print("\n⚠ last_error_message — Telegram не смог достучаться до URL:", err, file=sys.stderr)
    pending = info.get("pending_update_count") or 0
    if pending:
        print(f"\n⚠ В очереди {pending} необработанных апдейтов.", file=sys.stderr)


if __name__ == "__main__":
    main()
