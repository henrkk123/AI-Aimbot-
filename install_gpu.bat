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

echo Detected desire for SPEED.
echo We will reinstall PyTorch with NVIDIA CUDA support.
echo.
echo 1. Removing CPU version...
call .venv\Scripts\activate.bat
pip uninstall -y torch torchvision torchaudio

echo.
echo 2. Installing CUDA version (Stable)...
:: Using generic index-url for latest stable CUDA (likely 12.x for 50-series)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

echo.
echo ==================================================
echo    DONE. RUN 'train_model.bat' NOW.
echo    You should see "NVIDIA GPU" in the log.
echo ==================================================
pause
