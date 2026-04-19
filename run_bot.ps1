# Telegram bot: venv, deps, .env check, start.
# Run: double-click run_bot.bat OR: powershell -File run_bot.ps1

$ErrorActionPreference = "Stop"
try {
    if ($PSVersionTable.PSVersion.Major -lt 6) {
        chcp 65001 | Out-Null
    }
} catch {}
$Root = $PSScriptRoot
Set-Location $Root

$envFile = Join-Path $Root ".env"
if (-not (Test-Path $envFile)) {
    Copy-Item (Join-Path $Root ".env.example") $envFile -Force
    Write-Host "Created .env — add BOT_TOKEN from @BotFather, save, run again." -ForegroundColor Yellow
    exit 1
}

$pyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pyExe) {
    Write-Host "Python not in PATH. Install Python 3.10+ from python.org (check Add to PATH)." -ForegroundColor Red
    exit 1
}

$venv = Join-Path $Root ".venv"
$venvPy = Join-Path $venv "Scripts\python.exe"
$venvPip = Join-Path $venv "Scripts\pip.exe"

if (-not (Test-Path $venvPy)) {
    Write-Host "Creating .venv ..."
    & $pyExe -m venv $venv
}

Write-Host "Installing dependencies ..."
& $venvPip install -q --disable-pip-version-check -r (Join-Path $Root "requirements.txt")

& $venvPy -c "from pathlib import Path; from dotenv import load_dotenv; import os, sys; load_dotenv(Path('.env')); t=(os.getenv('BOT_TOKEN') or '').strip(); sys.exit(0 if len(t)>20 else 1)"

if ($LASTEXITCODE -ne 0) {
    Write-Host "BOT_TOKEN missing or too short in .env — put token on same line as BOT_TOKEN=" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting bot... Keep window open. Stop: Ctrl+C" -ForegroundColor Green
& $venvPy (Join-Path $Root "bot.py")
