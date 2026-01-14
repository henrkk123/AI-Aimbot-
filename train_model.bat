@echo off
title CV-Overlay Trainer
cls
echo ==================================================
echo    STARTING TRAINING UI
echo ==================================================

cd /d "%~dp0"

if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat

python gui_training.py

pause
