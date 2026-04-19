# Деплой бота на Beget

## Общий хостинг (тариф с сайтом, без VPS)

**Не подходит** для этого бота: нужен процесс, который **круглосуточно** крутится и опрашивает Telegram (**long polling**). На shared-хостинге обычно нельзя держать такой долгий Python-процесс.

## VPS на Beget — подходит

На VPS ты сам администратор: ставишь Python, клонируешь проект, настраиваешь **systemd**, бот работает 24/7.

### 1. Заказ VPS

В панели Beget закажи **VPS**, выбери ОС (удобнее **Ubuntu 22.04** или **Debian 12**).

### 2. Подключение по SSH

```bash
ssh root@IP_ТВОЕГО_VPS
```

(логин/пароль или ключ — как выдал Beget.)

### 3. Системные пакеты

```bash
apt update
apt install -y git python3 python3-venv python3-pip
```

### 4. Пользователь и каталог (не под root)

```bash
adduser --disabled-password botuser
su - botuser
mkdir -p ~/app && cd ~/app
git clone https://github.com/ahmed11551/analizEnglish.git .
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
nano .env
```

В `.env` одна важная строка (без кавычек, без пробелов вокруг `=`):

```env
BOT_TOKEN=твой_токен_от_BotFather
```

Сохрани (`Ctrl+O`, Enter, `Ctrl+X`).

Проверка:

```bash
.venv/bin/python check_token.py && echo OK
.venv/bin/python bot.py
```

Если в консоли пошёл лог и нет ошибок — в Telegram нажми **Start** у бота. Остановка теста: `Ctrl+C`.

### 5. Автозапуск через systemd

Под **root**:

```bash
sudo nano /etc/systemd/system/english-test-bot.service
```

Вставь (пути поправь под своего пользователя и каталог):

```ini
[Unit]
Description=Telegram English grammar test bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=botuser
Group=botuser
WorkingDirectory=/home/botuser/app/analizEnglish
ExecStart=/home/botuser/app/analizEnglish/.venv/bin/python bot.py
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
```

Если репозиторий лежит прямо в `~/app` без подпапки, `WorkingDirectory` и `ExecStart` должны указывать на ту папку, где лежат `bot.py` и `.env`.

Включи сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now english-test-bot
sudo systemctl status english-test-bot
```

Логи:

```bash
journalctl -u english-test-bot -f
```

### 6. Обновление кода

```bash
su - botuser
cd ~/app/analizEnglish
git pull
.venv/bin/pip install -r requirements.txt
exit
sudo systemctl restart english-test-bot
```

### 7. Webhook вместо polling

На VPS **polling нормален** и проще. Перевод на webhook имеет смысл, если хочешь вызывать бота только через HTTPS без открытого процесса опроса — это отдельная доработка кода.

---

**Итог:** на **Beget VPS** — да, закинуть и запустить можно по шагам выше. На **обычном хостинге Beget без VPS** — для этого бота нет.
