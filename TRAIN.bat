@echo off
title NEURAL EDGE - TRAINING SUITE
cls
color 0e
echo ==================================================
echo    NEURAL EDGE: TRAINING UI (RTX 50-READY)
echo ==================================================
echo.

if not exist .venv (
    echo [!] Environment not found. Running setup first...
    call UPDATE.bat
)

echo [1/1] LAUNCHING NEURAL TRAINER...
call .venv\Scripts\activate.bat
python gui_training.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Trainer crashed. Consider running 'UPDATE.bat'.
    pause
)
