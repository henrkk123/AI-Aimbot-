@echo off
title UNIVERSAL NVIDIA UNLOCKER (RTX 30/40/50 Series)
cls
echo ==================================================
echo    ENABLING GPU ACCELERATION (CUDA)
echo ==================================================
echo.

:: 1. Check if already active
:: FORCE MODE: We assume the user ran this because something is wrong.
:: We will clean EVERYTHING.

:: Call the Python Logic (It is smarter than Batch)
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat

python force_install.py

pause
