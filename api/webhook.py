"""
Vercel Serverless: приём webhook от Telegram (POST JSON = Update).
Маршрут: /api/webhook (один файл api/webhook.py — стандартный путь для Vercel).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from http.server import BaseHTTPRequestHandler

from telegram import Update

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("webhook")


def _check_secret(handler: BaseHTTPRequestHandler) -> bool:
    expected = (os.environ.get("WEBHOOK_SECRET") or "").strip()
    if not expected:
        return True
    got = (handler.headers.get("X-Telegram-Bot-Api-Secret-Token") or "").strip()
    return got == expected


async def _process_body(body: bytes) -> None:
    from bot import create_application

    app = create_application()
    await app.initialize()
    await app.start()
    try:
        data = json.loads(body.decode("utf-8"))
        upd = Update.de_json(data, app.bot)
        await app.process_update(upd)
        await asyncio.sleep(2.5)
    finally:
        await app.stop()
        await app.shutdown()


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"OK: English test bot webhook. POST Telegram updates to this URL."
        )

    def do_POST(self) -> None:
        if not _check_secret(self):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            log.warning("Неверный или отсутствует X-Telegram-Bot-Api-Secret-Token")
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length > 0 else b"{}"
        try:
            asyncio.run(_process_body(body))
        except Exception:
            log.exception("Ошибка обработки webhook")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
            return
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, fmt: str, *args: object) -> None:
        log.info("%s - %s", self.address_string(), fmt % args)
