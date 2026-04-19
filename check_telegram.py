"""Проверка доступа до api.telegram.org (без токена). Код 0 - ок, 1 - нет связи.

Если в .env задан TELEGRAM_PROXY, проверка идёт через него (как у бота).
Иначе - прямое TCP+TLS (нужен прямой доступ или системный VPN).
"""
from __future__ import annotations

import os
import socket
import ssl
import sys
from pathlib import Path

from dotenv import load_dotenv


def _load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env")


def _check_direct() -> None:
    host = "api.telegram.org"
    port = 443
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=25) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            tls.getpeercert()


def _check_via_proxy(proxy: str) -> None:
    import httpx

    with httpx.Client(proxy=proxy, timeout=30.0, verify=True) as client:
        r = client.get("https://api.telegram.org/", follow_redirects=True)
    if r.status_code >= 600:
        raise OSError(f"HTTP {r.status_code}")


def main() -> None:
    _load_env()
    proxy = (os.environ.get("TELEGRAM_PROXY") or "").strip()

    try:
        if proxy:
            _check_via_proxy(proxy)
            print("OK: через TELEGRAM_PROXY до api.telegram.org есть HTTPS.")
        else:
            _check_direct()
            print("OK: прямое соединение с api.telegram.org:443 (TLS).")
    except OSError as e:
        print("Нет связи с api.telegram.org:", e, file=sys.stderr)
        print(
            "Проверь интернет, VPN, фаервол, антивирус.",
            file=sys.stderr,
        )
        if not proxy:
            print(
                "Если Telegram только через локальный прокси (Clash, v2rayN): "
                "добавь в .env строку TELEGRAM_PROXY=http://127.0.0.1:ПОРТ "
                "(порт из настроек клиента; для socks5 см. README).",
                file=sys.stderr,
            )
        sys.exit(1)
    except ssl.SSLError as e:
        print("TLS-ошибка:", e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Ошибка проверки:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
