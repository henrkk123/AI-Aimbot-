@echo off
title NEURAL EDGE - START SYSTEM
cls
color 0d
echo ==================================================
echo    NEURAL EDGE: STARTING AI OVERLAY
echo ==================================================
echo.

if not exist .venv (
    echo [!] Environment not found. Running setup first...
    call UPDATE.bat
)

echo [1/1] LAUNCHING NEURAL EDGE...
call .venv\Scripts\activate.bat
python overlay.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] System crashed. Consider running 'UPDATE.bat'.
    pause
)
