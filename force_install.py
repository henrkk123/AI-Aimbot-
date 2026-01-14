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
    
    # 3.11 or 3.12 is the current sweet spot for the latest AI libraries.
    if major != 3 or minor < 11 or minor > 12:
        print("\n" + "!"*50)
        print("❌ CRITICAL ERROR: INCOMPATIBLE PYTHON VERSION!")
        print(f"   You are using Python {major}.{minor}.")
        print("   The latest AI Core (v0.6.2) requires Python 3.11 or 3.12.")
        print("\n   PLEASE DO THIS:")
        print("   1. Uninstall your current Python.")
        print("   2. Install Python 3.11.9 (The New Standard).")
        print("   🔗 Download: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe")
        print("   3. Make sure to check 'Add to PATH' during install!")
        print("!"*50 + "\n")
        time.sleep(3)
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

# 0.5 Upgrade Pip & Build Tools
print("Step 0.5: PREPARING ENVIRONMENT")
run_cmd(f"{py_pip} install --upgrade pip setuptools wheel")

# 1. Purge
print("Step 1: DEEP CLEANUP")
run_cmd(f"{py_pip} uninstall -y torch torchvision torchaudio ultralytics numpy customtkinter pynput mss opencv-python dxcam")
run_cmd(f"{py_pip} cache purge")

# 2. Install
print("\nStep 2: INSTALLING COMPATIBLE AI CORE (CUDA 12.8)")
# Ensure Blackwell support is flagged
os.environ["TORCH_CUDA_ARCH_LIST"] = "10.0;11.0;12.0" 

# Install main libraries
install_cmd = f"{py_pip} install --pre torch torchvision torchaudio ultralytics dxcam customtkinter pynput mss opencv-python triton --extra-index-url https://download.pytorch.org/whl/nightly/cu128"
run_cmd(install_cmd)

# 3. Verify
print("\nStep 3: FINAL VERIFICATION")
try:
    import torch
    import customtkinter
    import ultralytics
    print("✅ ALL LIBRARIES DETECTED.")
    
    if check_gpu():
        cap = torch.cuda.get_device_capability(0)
        if cap[0] >= 10:
            print("🚀 BLACKWELL (RTX 50) ARCHITECTURE ACTIVE!")
        print("\n✅ INSTALLATION SUCCESSFUL!")
    else:
        print("\n⚠️  GPU NOT DETECTED. The app will run on CPU.")
except Exception as e:
    print(f"\n❌ VERIFICATION FAILED: {e}")
    print("   Something went wrong during the library installation.")
    print("   1. Ensure your NVIDIA Driver is 570+ (RTX 50-Series requirement).")
    print("   2. Try running \"UPDATE.bat\" again as Administrator.")

input("\n[ALL DONE] Press Enter to finish...")
