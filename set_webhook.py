"""
Одноразово: зарегистрировать webhook у Telegram.
В .env или в окружении: BOT_TOKEN, WEBHOOK_URL (https://.../api/webhook), опционально WEBHOOK_SECRET.

  python set_webhook.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from config import BOT_TOKEN, WEBHOOK_SECRET, WEBHOOK_URL


def main() -> None:
    if not BOT_TOKEN:
        print("Нет BOT_TOKEN", file=sys.stderr)
        sys.exit(1)
    if not WEBHOOK_URL:
        print(
            "Задай WEBHOOK_URL, например https://твой-проект.vercel.app/api/webhook",
            file=sys.stderr,
        )
        sys.exit(1)

    api = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    payload: dict = {"url": WEBHOOK_URL}
    secret = (WEBHOOK_SECRET or "").strip()
    if secret:
        payload["secret_token"] = secret

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
    except urllib.error.HTTPError as e:
        print("HTTP ошибка:", e.read().decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Сеть:", e, file=sys.stderr)
        sys.exit(1)

    out = json.loads(raw.decode("utf-8"))
    if not out.get("ok"):
        print("Telegram ответил не ok:", out, file=sys.stderr)
        sys.exit(1)
    print("Webhook установлен:", WEBHOOK_URL)
    if secret:
        print("Секрет включён — в Vercel должен быть тот же WEBHOOK_SECRET.")


if __name__ == "__main__":
    main()
