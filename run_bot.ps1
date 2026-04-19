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
    Write-Host 'Created .env - add BOT_TOKEN from BotFather, save, run again.' -ForegroundColor Yellow
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

& $venvPy (Join-Path $Root "check_token.py")

if ($LASTEXITCODE -ne 0) {
    Write-Host 'BOT_TOKEN missing or too short in .env (same line as BOT_TOKEN=).' -ForegroundColor Yellow
    exit 1
}

$envRaw = Get-Content -LiteralPath $envFile -Raw -ErrorAction SilentlyContinue
if ($envRaw -match '(?m)^SKIP_TELEGRAM_CHECK=1\s*$') {
    Write-Host 'SKIP_TELEGRAM_CHECK=1 - skipping connectivity test.' -ForegroundColor Yellow
} else {
    & $venvPy (Join-Path $Root "check_telegram.py")
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Fix network/VPN or set TELEGRAM_PROXY in .env - see README (Troubleshooting).' -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Starting bot... Keep window open. Stop: Ctrl+C" -ForegroundColor Green
& $venvPy (Join-Path $Root "bot.py")
