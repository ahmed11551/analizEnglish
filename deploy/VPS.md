# Деплой на Linux VPS

Подойдёт любой VPS с SSH (Beget, Play2GO, Selectel, Hetzner и т.д.). Нужна ОС вроде **Ubuntu 22.04/24.04** или **Debian 12**.

## Обычный веб-хостинг без VPS

**Не подходит:** боту нужен процесс **24/7** с **long polling** к Telegram. На shared-хостинге так обычно нельзя.

## Шаги

### 1. Подключение по SSH

```bash
ssh root@IP_СЕРВЕРА
```

(логин и способ доступа — как в панели провайдера.)

### 2. Пакеты

```bash
apt update
apt install -y git python3 python3-venv python3-pip
```

### 3. Пользователь и проект (не под root)

```bash
adduser --disabled-password botuser
su - botuser
mkdir -p ~/app && cd ~/app
git clone https://github.com/ahmed11551/analizEnglish.git .
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
nano .env
```

В `.env`:

```env
BOT_TOKEN=твой_токен_от_BotFather
```

Проверка и ручной запуск:

```bash
.venv/bin/python check_token.py && echo OK
.venv/bin/python bot.py
```

Остановка: `Ctrl+C`.

### 4. systemd (автозапуск)

Под root создай `/etc/systemd/system/english-test-bot.service` — возьми за основу файл **`english-test-bot.service.example`** в этой папке, поправь `User`, `WorkingDirectory`, `ExecStart`.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now english-test-bot
sudo journalctl -u english-test-bot -f
```

### 5. Обновление

```bash
su - botuser
cd ~/app/analizEnglish
git pull
.venv/bin/pip install -r requirements.txt
exit
sudo systemctl restart english-test-bot
```

На VPS **polling** достаточен; webhook — отдельная доработка кода.
