# 🧪 CV-Overlay Pro v0.1.26 (The Purge)

> **✨ GPU FIX V3 (Final Boss)**
> "It still says CPU?!"
> The issue is `pip` cached the bad CPU version and keeps reinstalling it.

## 🛠️ The Fix
-   **Pip Cache Purge**: The installer now aggressively deletes your pip cache.
-   **Version Lock**: I forced it to download `torch==2.1.2+cu118` explicitly. It CANNOT pick the wrong one anymore.

## 📦 How to Apply
1.  **Download v0.1.26**.
2.  Run `install_gpu.bat` **FOR THE LAST TIME**.
3.  Watch it say "Purging Cache".
4.  Start Trainer.

*Diagnostics should now say: CUDA 11.8. Device: GPU.* 🤞

---

**Contributors**: @henrkk123
