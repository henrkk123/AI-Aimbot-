@echo off
title CV-Overlay Pro Launcher
cls
echo ==================================================
echo    LAUNCHING CV-OVERLAY PRO SYSTEM
echo ==================================================

cd /d "%~dp0"

:: Activate venv if exists
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat

:: Kill old instances
taskkill /F /IM python.exe /FI "WINDOWTITLE eq CV-Overlay-Backend" >nul 2>&1

:: Start Backend Hidden or Minimized
echo [1/2] Starting AI Core...
start "CV-Overlay-Backend" /min python server.py

timeout /t 3 /nobreak >nul

:: Start Frontend
echo [2/2] Starting Liquid UI...
cd overlay-ui
call npm run electron

:: Cleanup
echo Shutting down...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq CV-Overlay-Backend" >nul 2>&1
