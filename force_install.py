import subprocess
import sys
import os
import time

def run_cmd(cmd):
    print(f"👉 RUNNING: {cmd}")
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Command failed with code {e.returncode}")

def check_gpu():
    try:
        import torch
        print(f"\n🔍 DIAGNOSTICS:")
        print(f"   - Torch Version: {torch.__version__}")
        print(f"   - CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   - Device Name: {torch.cuda.get_device_name(0)}")
            print(f"   - CUDA Version: {torch.version.cuda}")
            return True
        else:
            return False
    except ImportError:
        return False

print("=========================================")
print("   NVIDIA GPU FORCE INSTALLER (PYTHON)")
print("=========================================")
print("This script will brutally fix your installation.")
print("It is designed for RTX 50-Series (Blackwell).")
print("")

# 0. Environment Check
print(f"👉 RUNNING IN: {sys.prefix}")
print(f"👉 PYTHON EXE: {sys.executable}")
if ".venv" not in sys.prefix and "venv" not in sys.prefix:
    print("⚠️  WARNING: You might not be in the .venv!")
    print("    Continuing anyway...")

# 1. Purge
print("Step 1: CLEANUP")
py_pip = f'"{sys.executable}" -m pip'
run_cmd(f"{py_pip} uninstall -y torch torchvision torchaudio ultralytics numpy")
run_cmd(f"{py_pip} cache purge")

# 2. Install
print("\nStep 2: INSTALLING NIGHTLY (CUDA 12.6)")
install_cmd = f'{py_pip} install --pre torch torchvision torchaudio ultralytics numpy --extra-index-url https://download.pytorch.org/whl/nightly/cu126'
run_cmd(install_cmd)

# 3. Verify
print("\nStep 3: VERIFICATION")
if check_gpu():
    print("\n✅ SUCCESS! YOUR GPU IS ACTIVE.")
    print("   You are ready to train.")
else:
    print("\n❌ FAILURE. Still seeing CPU?")
    print("   Please screenshot this window and send it to developer.")

input("\nPress Enter to exit...")
