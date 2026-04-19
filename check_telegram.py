"""Проверка TCP+TLS до api.telegram.org (без токена). Код 0 — связь есть, 1 — нет."""
from __future__ import annotations

import socket
import ssl
import sys


def main() -> None:
    host = "api.telegram.org"
    port = 443
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=25) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as tls:
                tls.getpeercert()
    except OSError as e:
        print("Нет связи с", f"{host}:{port}:", e, file=sys.stderr)
        print(
            "Проверь интернет, VPN, фаервол Windows, антивирус. "
            "Если без VPN Telegram не открывается — включи VPN и при необходимости "
            "добавь в .env: TELEGRAM_PROXY=http://127.0.0.1:ПОРТ (или socks5://...).",
            file=sys.stderr,
        )
        sys.exit(1)
    except ssl.SSLError as e:
        print("TLS-ошибка до api.telegram.org:", e, file=sys.stderr)
        sys.exit(1)
    print("OK: соединение с api.telegram.org:443 (TLS) установлено.")


if __name__ == "__main__":
    main()
