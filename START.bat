@echo off
title AXION ENGINE - START SYSTEM v0.7.7
cls
color 0a
echo ==================================================
echo    AXION CORE: INITIALIZING NEURAL HUD
echo ==================================================
echo.

if not exist .venv (
    echo [!] AI Environment not found. Running autostart...
    call UPDATE.bat
)

echo [1/1] ACTIVATING BLACKWELL KERNELS...
call .venv\Scripts\activate.bat
python overlay.py

if %errorlevel% neq 0 (
    echo.
    echo [❌] SYSTEM CRASH DETECTED.
    echo [!] Running 'UPDATE.bat' to repair the environment is recommended.
    pause
)
