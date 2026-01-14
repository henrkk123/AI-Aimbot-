@echo off
title CV-Overlay Pro Launcher
cls
echo ==================================================
echo    LAUNCHING CV-OVERLAY PRO SYSTEM
echo ==================================================
cd /d "%~dp0"

:: 1. Check commands
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'python' command not found!
    echo Please install Python and check "Add to PATH".
    pause
    exit /b 1
)
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'npm' command not found!
    echo Please install Node.js.
    pause
    exit /b 1
)

:: 2. Activate Venv
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [WARN] No .venv found. Using system python.
)

:: 3. Check & Auto-Heal Dependencies
REM we always enforce python libs now to catch missing updates like customtkinter
if not exist .venv (
    echo [1/2] Creating Python Brain...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python customtkinter packaging pillow

:: Node Setup (only if missing)
if not exist "overlay-ui\node_modules\" (
    echo [2/2] Installing Liquid UI...
    cd overlay-ui
    call npm install
    cd ..
)

echo [✅] System Ready. Launching...
echo.

:: 4. Kill old
taskkill /F /IM python.exe /FI "WINDOWTITLE eq CV-Overlay-Backend" >nul 2>&1

:: 5. Launch Backend
echo [1/2] Starting AI Core...
start "CV-Overlay-Backend" /min python server.py

echo Waiting for warmup...
timeout /t 3 /nobreak >nul

:: 6. Launch Frontend
echo [2/2] Starting Liquid UI...
cd overlay-ui
REM We use dev:all to run Vite + Electron together
call npm run dev:all
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed.
    pause
)

:: Cleanup
taskkill /F /IM python.exe /FI "WINDOWTITLE eq CV-Overlay-Backend" >nul 2>&1
exit /b 0
