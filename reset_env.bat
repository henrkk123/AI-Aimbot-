@echo off
title FACTORY RESET
cls
echo ==================================================
echo    FACTORY RESET (DELETE VENV)
echo ==================================================
echo.
echo This will DELETE your Python environment (.venv).
echo It forces a full re-download next time you start.
echo.
echo THIS IS THE NUCLEAR OPTION.
echo.
pause

echo.
if exist .venv (
    echo Deleting .venv...
    rmdir /s /q .venv
) else (
    echo .venv not found.
)

echo.
echo CLEANUP COMPLETE.
echo Now run 'install_gpu.bat' to start fresh.
echo.
pause
