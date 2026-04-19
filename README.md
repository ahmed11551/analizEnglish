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

```bash
cd analiz
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

В `.env` укажи `BOT_TOKEN` (и при желании `BRAND_TITLE`, `BRAND_SUBTITLE`).

```bash
python bot.py
```

Команды меню (`/start`, `/help`, `/cancel`, `/skip`) подставляются при старте бота автоматически.

## Переменные окружения

| Переменная | Обязательно | Описание |
|------------|-------------|----------|
| `BOT_TOKEN` | да | Токен от BotFather |
| `BRAND_TITLE` | нет | Заголовок в приветствии |
| `BRAND_SUBTITLE` | нет | Подзаголовок |
| `LOG_LEVEL` | нет | `INFO` (по умолчанию), `DEBUG` и т.д. |

## Деплой на сервер (Beget VPS и др.)

Пошагово: **[deploy/BEGET.md](deploy/BEGET.md)** (VPS, systemd, обновления). Обычный shared-хостинг без VPS для этого бота не подходит.

## Структура

- `bot.py` — логика Telegram
- `questions_data.py` — вопросы, ключи, тексты уровней
- `config.py` — загрузка `.env`
- `deploy/` — инструкции и пример unit для Linux
