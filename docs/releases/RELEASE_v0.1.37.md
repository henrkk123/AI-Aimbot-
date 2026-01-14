# 🐉 CV-Overlay Pro v0.1.37 (BLACKWELL EDITION)

> **🚀 UNLOCKING RTX 50-SERIES POTENTIAL.**

## 🛠️ The Fix
We identified that the RTX 5070 (Blackwell) was hitting a "No kernel image" error because PyTorch libraries were too old for the new hardware.

### 1. CUDA 12.8 Support
The installer (`UPDATE.bat`) now fetches the **Absolute Latest Nightly Build (cu128)**. 
This includes the kernels for Blackwell (`sm_120`).

### 2. Training Stability
-   Fixed dataset structure (Proper `images/` and `labels/` subfolders).
-   Reduced resource intensity (Batch 16, Cache Off) to prevent hangs.

## ⚠️ MANDATORY STEP
To use this, you **MUST** update your NVIDIA Driver to **version 570.xx or higher**.
Without the new driver, the GPU won't recognize the CUDA 12.8 instructions.

*Ride the lightning.*

---
**Status**: Beta (Blackwell Support Active)
