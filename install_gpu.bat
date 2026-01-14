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
echo 2. Installing CUDA 11.8 (Force Version 2.1.2)...
:: Explicitly forcing the +cu118 wheel to prevent CPU fallback
pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 torchaudio==2.1.2+cu118 --index-url https://download.pytorch.org/whl/cu118

echo.
echo ==================================================
echo    DONE. RUN 'train_model.bat' NOW.
echo    You should see "NVIDIA GPU" in the log.
echo ==================================================
pause
