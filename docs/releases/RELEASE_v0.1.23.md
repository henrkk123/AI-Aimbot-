# 📉 CV-Overlay Pro v0.1.23 (Compatibility Mode)

> **✨ GPU FIX V2 (The Classic)**
> "CUDA 12.4 didn't work?"
> I'm downgrading to **CUDA 11.8**. This is the version that *always* works.

## 🛠️ The Fix
-   **Old is Gold**: Newer CUDA versions (12.x) sometimes hate YOLOv8.
-   **Downgrade**: `install_gpu.bat` now installs `cu118` (CUDA 11.8).
-   This removes the "0% Usage" bug for 99% of people.

## 📦 How to Apply
1.  **Download v0.1.23**.
2.  Run `install_gpu.bat` **AGAIN**.
3.  Let it uninstall the 12.4 junk and install 11.8.
4.  Start Trainer.

*If this doesn't work, nothing will.* 💀

---

**Contributors**: @henrkk123
