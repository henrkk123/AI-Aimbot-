@echo off
title AXION ENGINE - ULTIMATE STABILITY v0.7.7
cls
color 0a

:: Force working directory
cd /d "%~dp0"

echo --------------------------------------------------
echo    AXION CORE: ULTIMATE INSTALLER v0.7.7
echo --------------------------------------------------
echo.
echo [!] This is the high-stability version for Axion 0.7.
echo.

echo [STEP 1/4] CLEANING PROCESSES...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM AxionEngine.exe /T 2>nul

echo [STEP 2/4] WIPING OLD ENVIRONMENT...
if exist .venv rmdir /s /q .venv

echo [STEP 3/4] LOCATING PYTHON...
set "BEST_PY="

:: TRY 3.11
py -3.11 -c "import sys" >nul 2>&1
if %errorlevel% equ 0 (
    set "BEST_PY=py -3.11"
    echo [+] Using Python 3.11
    goto CREATE_VENV
)

:: TRY 3.12
py -3.12 -c "import sys" >nul 2>&1
if %errorlevel% equ 0 (
    set "BEST_PY=py -3.12"
    echo [+] Using Python 3.12
    goto CREATE_VENV
)

:: TRY DEFAULT
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "BEST_PY=python"
    echo [+] Using default python command
    goto CREATE_VENV
)

:PYTHON_FAIL
echo.
echo [❌] FATAL ERROR: Python 3.11/3.12 NOT FOUND.
echo [!] PLEASE INSTALL: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
echo.
pause
exit /b 1

:CREATE_VENV
%BEST_PY% -m venv .venv
if %errorlevel% neq 0 (
    echo [❌] VENV CREATION FAILED.
    pause
    exit /b 1
)

echo [STEP 4/4] STARTING CORE INSTALLATION...
if not exist "force_install.py" (
    echo [❌] ERROR: force_install.py missing in %cd%
    pause
    exit /b 1
)

".venv\Scripts\python.exe" force_install.py
if %errorlevel% neq 0 (
    echo.
    echo [❌] SUB-INSTALLER FAILED. Check errors above.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo    ✅ AXION CORE v0.7.7 IS READY.
echo ==================================================
timeout /t 5
exit /b 0
