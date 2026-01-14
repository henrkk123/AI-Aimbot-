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
set PYTHON_EXE=python

:: Check for Python Launcher (py.exe) with specific versions
py -3.11 -c "import sys" >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=py -3.11
    echo [+] Using Python 3.11 Launcher
) else (
    py -3.12 -c "import sys" >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_EXE=py -3.12
        echo [+] Using Python 3.12 Launcher
    ) else (
        echo [!] Warning: Python Launcher not found or 3.11/3.12 not installed via py.exe.
        echo [!] Falling back to default 'python' command...
    )
)

%PYTHON_EXE% -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Virtual environment creation failed!
    echo [TIP] Try installing Python 3.11 manually from python.org.
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
