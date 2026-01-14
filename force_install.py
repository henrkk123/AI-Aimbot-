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

def check_driver():
    try:
        output = subprocess.check_output("nvidia-smi --query-gpu=driver_version --format=csv,noheader", shell=True).decode().strip()
        major = int(output.split('.')[0])
        print(f"👉 NVIDIA DRIVER DETECTED: {output}")
        if major < 570:
            print("❌ WARNING: Your driver is too old for RTX 50-Series!")
            print("   Please install Driver 570.xx or higher from nvidia.com.")
            return False
        return True
    except:
        print("⚠️  Warning: Could not detect NVIDIA driver version. Ensure it is 570+.")
        return True

def check_python_version():
    major, minor = sys.version_info.major, sys.version_info.minor
    print(f"👉 PYTHON VERSION: {sys.version.split()[0]}")
    
    # 3.10 and 3.11 are the "Golden" versions for AI libraries.
    # 3.12 is okay for some, but 3.13 is way too new for torch nightly.
    if major != 3 or minor < 10 or minor > 12:
        print("\n" + "!"*50)
        print("❌ CRITICAL ERROR: WRONG PYTHON VERSION!")
        print(f"   You are using Python {major}.{minor}.")
        print("   AI libraries (Torch/YOLO) HATE this version.")
        print("\n   PLEASE DO THIS:")
        print("   1. Uninstall your current Python.")
        print("   2. Install Python 3.10.11 (The Golden Version).")
        print("   🔗 Download: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe")
        print("   3. Make sure to check 'Add to PATH' during install!")
        print("!"*50 + "\n")
        time.sleep(2)
        return False
    return True

# 0. System Check
print(f"👉 RUNNING IN: {sys.prefix}")
print(f"👉 PYTHON EXE: {sys.executable}")
if not check_python_version():
    input("Press Enter to close and fix your Python version...")
    sys.exit(1)

check_driver()

py_pip = f'"{sys.executable}" -m pip'

# 0.5 Upgrade Pip (Fixes most "No matching distribution" errors)
print("Step 0.5: UPGRADING PIP")
run_cmd(f"{py_pip} install --upgrade pip")
print("Step 1: CLEANUP")
run_cmd(f"{py_pip} uninstall -y torch torchvision torchaudio ultralytics numpy")
run_cmd(f"{py_pip} cache purge")

# 2. Install
print("\nStep 2: INSTALLING BLACKWELL-READY NIGHTLY (CUDA 12.8)")
print("👉 Target: sm_120 / RTX 50-Series Support")
# Signal Blackwell support to pip/torch during install
os.environ["TORCH_CUDA_ARCH_LIST"] = "10.0;11.0;12.0" 
install_cmd = f'{py_pip} install --pre torch torchvision torchaudio ultralytics numpy dxcam triton setuptools --extra-index-url https://download.pytorch.org/whl/nightly/cu128'
run_cmd(install_cmd)

# 3. Verify
print("\nStep 3: VERIFICATION")
if check_gpu():
    import torch
    cap = torch.cuda.get_device_capability(0)
    print(f"   - Compute Capability: {cap}")
    if cap[0] >= 10:
        print("🚀 BLACKWELL ARCHITECTURE DETECTED & ACTIVE!")
    
    print("\n✅ SUCCESS! YOUR GPU IS ACTIVE.")
    print("   Optimization: CUDA 12.8 / SM_120 (RTX 50 Edition)")
else:
    # ...
    print("\n❌ FAILURE. Still seeing CPU?")
    print("   1. Update your NVIDIA Driver (570+ required).")
    print("   2. Run this script again.")

input("\nPress Enter to exit...")
