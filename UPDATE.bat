@echo off
title SYSTEM UPDATE & REPAIR
cls
color 0b
echo ==================================================
echo    CV-OVERLAY: SYSTEM UPDATE & REPAIR
echo ==================================================
echo.
echo This will:
echo 1. DELETE existing environments (Factory Reset).
echo 2. DOWNLOAD the latest Nightly AI drivers (RTX 5070+).
echo 3. VERIFY your GPU.
echo.
echo [!] Only run this if something is broken or you want to upgrade.
echo.
pause

call reset_env.bat
call install_gpu.bat

echo.
echo ==================================================
echo    UPDATE COMPLETE.
echo    You can now run 'START.bat'.
echo ==================================================
pause
