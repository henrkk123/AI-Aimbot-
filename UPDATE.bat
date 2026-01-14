@echo off
title NEURAL EDGE - SYSTEM REPAIR
cls
color 0b
echo ==================================================
echo    NEURAL EDGE: SYSTEM REPAIR & GPU SETUP
echo ==================================================
echo.
echo This will:
echo 1. WIPE your current AI environment.
echo 2. INSTALL Blackwell-ready drivers (RTX 5070+).
echo 3. OPTIMIZE performance for your GPU.
echo.
echo [!] Ensure you have the latest NVIDIA Drivers installed.
echo.
pause

echo [1/3] CLEANING OLD ENVIRONMENT...
taskkill /F /IM python.exe /T >nul 2>&1
if exist .venv (
    rmdir /s /q .venv
)

echo [2/3] CREATING FRESH BRAIN...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Python not found or venv creation failed!
    pause
    exit /b 1
)

echo [3/3] RUNNING DEEP INSTALLER...
call .venv\Scripts\activate.bat
python force_install.py

echo.
echo ==================================================
echo    INSTALLATION COMPLETE.
echo    You can now run 'START.bat'.
echo ==================================================
pause
