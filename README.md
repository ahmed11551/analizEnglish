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

## Деплой на VPS

**[deploy/VPS.md](deploy/VPS.md)** — SSH, venv, systemd, обновления. Shared-хостинг без VPS не подходит.

## Структура

- `bot.py` — логика Telegram
- `questions_data.py` — вопросы, ключи, тексты уровней
- `config.py` — загрузка `.env`
- `deploy/` — инструкции и пример unit для Linux
