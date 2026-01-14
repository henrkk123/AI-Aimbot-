@echo off
title UNIVERSAL NVIDIA UNLOCKER (RTX 30/40/50 Series)
cls
echo ==================================================
echo    ENABLING GPU ACCELERATION (CUDA)
echo ==================================================
echo.

:: 1. Check if already active
if exist .venv (
    call .venv\Scripts\activate.bat
    python -c "import torch; exit(0) if torch.cuda.is_available() else exit(1)"
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ GREAT NEWS: Your GPU is ALREADY working!
        echo    No need to reinstall anything.
        echo.
        pause
        exit /b
    )
)

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
