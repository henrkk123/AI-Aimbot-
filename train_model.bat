@echo off
title CV-Overlay Trainer
cls
echo ==================================================
echo    STARTING TRAINING UI
echo ==================================================
cd /d "%~dp0"

:: Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'python' command not found!
    echo Please install Python and check "Add to PATH".
    pause
    exit /b 1
)

:: Activate Venv
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [WARN] No .venv found. Using system python.
)

echo [INFO] Ensuring Trainer Dependencies...
pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python customtkinter packaging pillow

python gui_training.py

echo.
echo Process ended.
pause
