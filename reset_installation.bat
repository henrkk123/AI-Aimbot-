@echo off
title CV-Overlay Factory Reset
cls
echo ==================================================
echo    FACTORY RESET TOOL
echo ==================================================
echo.
echo This will DELETE:
echo  - Python Virtual Environment (.venv)
echo  - UI Dependencies (node_modules)
echo.
echo It will NOT delete your models or code.
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/2] Removing Python Environment...
if exist .venv (
    rmdir /s /q .venv
    echo [OK] .venv deleted.
) else (
    echo [SKIP] .venv not found.
)

echo.
echo [2/2] Removing Node Modules...
if exist overlay-ui\node_modules (
    rmdir /s /q overlay-ui\node_modules
    echo [OK] node_modules deleted.
) else (
    echo [SKIP] node_modules not found.
)

echo.
echo ==================================================
echo    RESET COMPLETE.
echo    Please run 'start_overlay.bat' to reinstall.
echo ==================================================
pause
