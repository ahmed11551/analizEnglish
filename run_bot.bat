@echo off
chcp 65001 >nul
cd /d "%~dp0"
title English Test Bot
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_bot.ps1"
if errorlevel 1 pause
