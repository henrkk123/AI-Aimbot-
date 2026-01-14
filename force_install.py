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

# 0. System Check
print(f"👉 RUNNING IN: {sys.prefix}")
print(f"👉 PYTHON EXE: {sys.executable}")
check_driver()

# 1. Purge
# ... (rest of the script remains same, just adding packages to install_cmd) ...
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
