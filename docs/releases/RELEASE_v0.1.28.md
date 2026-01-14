# 🔒 CV-Overlay Pro v0.1.28 (The Lock)

> **✨ CONFLICT RESOLUTION**
> "I installed the GPU fix, but the Launcher broke it!"
> Fixed.

## 🛠️ The Bug
-   `install_gpu.bat` installed the cool Nightly GPU version.
-   `start_overlay.bat` saw "Unknown Version", panicked, and re-installed the boring CPU version.

## 🛠️ The Fix
-   **Smart Lock**: All launchers now check if you have the libraries first.
-   **If found**: They do NOTHING. They touch nothing. Your GPU driver stays safe.
-   **Install_GPU**: Now installs `ultralytics` too, creating a unified unbreakable dependency tree.

## 📦 How to Apply
1.  **Download v0.1.28**.
2.  Run `install_gpu.bat` **ONE LAST TIME**.
3.  Launch normally. It will skip the "Installing..." step and finally work.

*We got him.* 🕵️‍♂️

---

**Contributors**: @henrkk123
