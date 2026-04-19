# Деплой на Vercel (webhook)

На Vercel **нельзя** использовать long polling. Бот работает через **HTTPS webhook**: Telegram шлёт POST на `/api/webhook`.

## Ограничения serverless

- Функция на каждый апдейт может стартовать **холодно** — без стабильного хранилища сессия теста может **сброситься** между сообщениями.
- Включи **`PERSISTENCE_PATH=/tmp/ptb.pkl`** в переменных Vercel: состояние `user_data` пишется в файл `/tmp` **на том же инстансе**. При **другом** инстансе или холодном старте прогресс может обнулиться. Для гарантированной стабильности лучше **VPS** (см. `VPS.md`).
- Лиды: задай **`LEADS_FILE=/tmp/leads.jsonl`**, иначе запись в `data/` на Vercel может быть недоступна.

## Шаги

### 1. Репозиторий на GitHub

Проект уже заточен под корень репозитория (`bot.py`, `api/webhook/index.py`, `requirements.txt`).

**Импорт в Vercel:** в шаге выбора фреймворка лучше указать **Other** (не только «Python»), чтобы корректно подхватились serverless-файлы в каталоге `api/`. Если сборка ругалась на `vercel.json` → `functions`, в репозитории используется glob `api/**/*.py` и вложенный `api/webhook/index.py` под маршрут `/api/webhook`.

### 2. Проект в Vercel

1. Зайди на [vercel.com](https://vercel.com) → **Add New** → **Project** → импорт репозитория.
2. **Framework Preset**: Other (или автоматически определит Python).
3. **Environment Variables** (Production): список ключей и заготовки значений — в репозитории **[env.vercel.template](env.vercel.template)** (скопируй как `deploy/env.vercel.local`, заполни, перенеси в панель; `env.vercel.local` в git не попадёт).

| Переменная | Обязательно | Пример / комментарий |
|------------|-------------|----------------------|
| `BOT_TOKEN` | да | токен от @BotFather |
| `WEBHOOK_SECRET` | рекомендуется | случайная строка 16–64 символа (буквы, цифры, `_`, `-`) |
| `PERSISTENCE_PATH` | рекомендуется | `/tmp/ptb.pkl` |
| `LEADS_FILE` | для лидов | `/tmp/leads.jsonl` |
| `BRAND_TITLE`, `BRAND_SUBTITLE` | нет | как в `.env.example` |
| `TELEGRAM_PROXY` | нет | если Vercel-регион не достучится до Telegram (редко) |

4. **Deploy**.

5. Скопируй URL деплоя, например `https://analiz-english-xxx.vercel.app`.

### 3. Установить webhook

На **своём ПК** (где есть доступ к `api.telegram.org`) в корне проекта в `.env` временно добавь:

```env
WEBHOOK_URL=https://ТВОЙ-ПРОЕКТ.vercel.app/api/webhook
WEBHOOK_SECRET=тот_же_секрет_что_в_Vercel
BOT_TOKEN=...
```

Затем:

```bash
python set_webhook.py
```

Либо вручную `POST https://api.telegram.org/bot<TOKEN>/setWebhook` с JSON `{"url":"...","secret_token":"..."}`.

Проверка: открой в браузере `https://ТВОЙ-ПРОЕКТ.vercel.app/api/webhook` — должен быть текст **OK: English test bot webhook...**

### 4. Снять webhook (вернуться на polling локально)

```bash
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
```

---

**Итог:** Vercel подходит для **демо и лёгкой нагрузки**; для стабильного продакшена с лидами и длинными сессиями надёжнее **VPS + polling** или внешнее Redis-хранилище (отдельная доработка).
