@echo off
setlocal enabledelayedexpansion
title AXION ENGINE - ULTIMATE CORE SETUP
cls
color 0b

:: Set working directory to the script folder
cd /d "%~dp0"

echo ==================================================
echo    AXION ENGINE: ULTIMATE REPAIR v0.6.1
echo ==================================================
echo.
echo [!] This will nuked your old setup and reinstall everything.
echo [!] Ensure you have NVIDIA Driver 570+ installed for RTX 5070.
echo.
pause

echo [1/4] TERMINATING OLD PROCESSES...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM AxionEngine.exe /T >nul 2>&1

echo [2/4] WIPING OLD BRAIN...
if exist .venv (
    rmdir /s /q .venv
)

echo [3/4] SEARCHING FOR VALID PYTHON (3.11/3.12)...
set PY_CMD=
py -3.11 -c "import sys" >nul 2>&1
if !errorlevel! equ 0 (
    set PY_CMD=py -3.11
    echo [+] FOUND: Python 3.11
) else (
    py -3.12 -c "import sys" >nul 2>&1
    if !errorlevel! equ 0 (
        set PY_CMD=py -3.12
        echo [+] FOUND: Python 3.12
    )
)

if "!PY_CMD!"=="" (
    echo.
    echo [❌] FATAL ERROR: VALID PYTHON NOT FOUND!
    echo [!] Axion Engine requires Python 3.11 or 3.12.
    echo [!] Your current version is either too old or too new (3.13).
    echo.
    echo [1] PLEASE INSTALL THIS: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo [2] RESTART THIS SCRIPT AFTER INSTALL.
    echo.
    pause
    exit /b 1
)

echo [+] Creating Virtual Environment...
!PY_CMD! -m venv .venv
if !errorlevel! neq 0 (
    echo [❌] ERROR: VENV CREATION FAILED.
    pause
    exit /b 1
)

echo [4/4] LAUNCHING DEEP CORE INSTALLER...
if not exist "%~dp0force_install.py" (
    echo [❌] FATAL ERROR: force_install.py NOT FOUND IN %~dp0
    pause
    exit /b 1
)

".venv\Scripts\python.exe" "%~dp0force_install.py"
if !errorlevel! neq 0 (
    echo.
    echo [❌] SETUP FAILED DURING LIBRARY INSTALL.
    echo [!] Read the errors above and try again.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo    ✅ AXION ENGINE DEPLOYED SUCCESSFULLY.
echo    You can now close this and run "START.bat".
echo ==================================================
pause
