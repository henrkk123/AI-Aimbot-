@echo off
title CV-Overlay Setup Script
cls
echo ==================================================
echo    INSTALLING DEPENDENCIES (Windows)
echo ==================================================
cd /d "%~dp0"

:: 1. Check Prereqs
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js/npm not found! Please install Node.js 18+.
    pause
    exit /b 1
)

:: 2. Setup Python Venv
echo.
echo [1/3] Setting up Python Environment...
if not exist .venv (
    python -m venv .venv
    echo Created .venv
)
call .venv\Scripts\activate.bat
echo Installing Python libs...
pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python customtkinter packaging pillow

:: 3. Setup Node
echo.
echo [2/3] Installing UI Dependencies (This may take a moment)...
cd overlay-ui
if exist node_modules rmdir /s /q node_modules
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] NPM Install failed.
    echo Please check your internet connection or Node installation.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ==================================================
echo    SETUP COMPLETE!
echo    You can now run start_overlay.bat
echo ==================================================
pause
exit /b 0
