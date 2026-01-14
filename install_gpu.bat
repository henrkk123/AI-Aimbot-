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
echo 1. Cleaning Cache & Removing CPU version...
call .venv\Scripts\activate.bat
pip cache purge
pip uninstall -y torch torchvision torchaudio numpy

echo.
echo 2. Installing PREVIEW Version (RTX 50-Series Support)...
:: RTX 5070 (SM_120) requires PyTorch Nightly + CUDA 12.6
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu126

echo.
echo ==================================================
echo    DONE. RUN 'train_model.bat' NOW.
echo    You should see "NVIDIA GPU" in the log.
echo ==================================================
pause
