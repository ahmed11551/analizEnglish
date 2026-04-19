# Тест английского · Grammar Check (Telegram-бот)

Бот проводит анкету, тест из 21 вопроса с темами, выставляет уровень (Pre-A1 … B2+) и список тем для повторения по ошибкам.

## Безопасность

- Токен бота **никогда** не публикуй в чатах, скриншотах и репозитории.
- Если токен мог утечь: [@BotFather](https://t.me/BotFather) → твой бот → **Revoke current token** → выпусти новый и положи только в локальный `.env`.

## Быстрый запуск (Windows)

1. Один раз заполни `.env`: строка `BOT_TOKEN=…` от [@BotFather](https://t.me/BotFather), сохрани файл.
2. Дважды щёлкни **`run_bot.bat`**  
   Или в PowerShell: `.\run_bot.ps1`  
   Скрипт сам создаст `.venv`, поставит зависимости и запустит `bot.py`.

В **Cursor / VS Code**: `Terminal` → `Run Task…` → **Run Telegram bot**.

## Запуск вручную

Создай `.venv`, `pip install -r requirements.txt`, заполни `.env`, затем `python bot.py` из корня проекта.

Команды меню в Telegram задаются при старте бота автоматически.

## Переменные окружения

| Переменная | Обязательно | Описание |
|------------|-------------|----------|
| `BOT_TOKEN` | да | Токен от BotFather |
| `BRAND_TITLE` | нет | Заголовок в приветствии |
| `BRAND_SUBTITLE` | нет | Подзаголовок |
| `LOG_LEVEL` | нет | `INFO` (по умолчанию), `DEBUG` и т.д. |
| `LEADS_FILE` | нет | Путь к файлу лидов; по умолчанию `data/leads.jsonl` |
| `TELEGRAM_PROXY` | нет | Прокси для Bot API, например `http://127.0.0.1:7890` или `socks5://127.0.0.1:1080` |
| `WEBHOOK_URL` | нет | Только для `set_webhook.py` (полный URL `/api/webhook` на Vercel) |
| `WEBHOOK_SECRET` | нет | Общий секрет Vercel + `setWebhook`; проверяется в `api/webhook.py` |
| `PERSISTENCE_PATH` | нет | Для Vercel: `/tmp/ptb.pkl` (см. VERCEL.md) |

После теста контакты и отказ от контакта (`/skip`) дописываются в **`data/leads.jsonl`** (каталог в `.gitignore`). На сервере делай бэкап и ограничивай доступ к файлу.

## Нет связи с Telegram (`ConnectError`, таймауты)

1. В каталоге проекта выполни: `.\.venv\Scripts\python.exe check_telegram.py` — проверка **TCP+TLS** до `api.telegram.org`.
2. Временно отключи **VPN** или, наоборот, **включи** (если без VPN маршрут до Telegram плохой).
3. Проверь **брандмауэр Windows** и **антивирус** (разреши Python исходящие HTTPS).
4. Другая сеть: **раздача с телефона** — быстрый тест, «виноват» ли домашний провайдер.
5. Если нужен **локальный прокси** (Clash, v2rayN и т.п.) — пропиши в `.env`: `TELEGRAM_PROXY=http://127.0.0.1:ПОРТ` (порт возьми из настроек клиента; для **SOCKS5** зависимость уже в `requirements.txt` через `[socks]`). После этого **`check_telegram.py`** проверяет связь **через этот же прокси** (как и сам бот).

Скрипт **`run_bot.ps1`** перед стартом запускает `check_telegram.py`. Чтобы **отключить** эту проверку (на свой риск): в `.env` строка `SKIP_TELEGRAM_CHECK=1`. Запуск **напрямую** `python bot.py` проверку не делает; при старте бот с `bootstrap_retries=-1` будет повторять подключение — **Ctrl+C** для остановки.

## Деплой на VPS

**[deploy/VPS.md](deploy/VPS.md)** — SSH, venv, systemd, обновления. Shared-хостинг без VPS не подходит.

## Деплой на Vercel (webhook)

**[deploy/VERCEL.md](deploy/VERCEL.md)** — переменные окружения, `set_webhook.py`, ограничения serverless. Для стабильной работы теста без сбоев сессии предпочтительнее VPS. Шаблон переменных для панели Vercel: **[deploy/env.vercel.template](deploy/env.vercel.template)**; локальный `.env` — из **`.env.example`**.

## Структура

- `bot.py` — логика Telegram
- `questions_data.py` — вопросы, ключи, тексты уровней
- `config.py` — загрузка `.env`
- `intro_validate.py` — проверка ответов анкеты
- `leads.py` — запись лидов в JSON Lines
- `check_telegram.py` — проверка доступа до `api.telegram.org`
- `api/webhook.py` — endpoint для Vercel (Telegram webhook)
- `set_webhook.py` — регистрация webhook у Telegram
- `deploy/` — VPS, Vercel
