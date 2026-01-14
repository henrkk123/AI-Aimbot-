# 🚑 CV-Overlay Pro v0.1.1 (Hotfix)

This release addresses critical setup and display issues reported by Windows users.

> **Upgrade Highly Recommended for Windows Users!**

---

## 🛠️ Major Fixes

### 🪟 Windows Setup Automation
-   **New Script**: `setup_windows.bat` automatically installs Python libraries AND Node.js dependencies.
-   **Fail-Safe**: Launchers now pause and explain exactly what is missing instead of just closing.

### 👻 Overlay Visibility
-   **Blank Screen Fix**: Fixed an issue where the overlay would start without the UI engine, showing a blank/transparent box.
-   **Sizing**: The overlay now correctly covers the **entire screen** (including taskbar area) to ensure perfect alignment with games.

---

## 📦 How to Update

1.  **Download Source Code** (zip) or `git pull`.
2.  **Run ONE TIME**: Double-click `setup_windows.bat`.
3.  **Launch**: Double-click `start_overlay.bat`.

---

## 📝 Changelog

-   [FIX] Added `setup_windows.bat` for one-click dependency installation.
-   [FIX] Hardened `start_overlay.bat` and `train_model.bat` with error trapping.
-   [FIX] Corrected Electron `npm run dev:all` command in launchers.
-   [FIX] Updated Electron `main.cjs` to use `screen.bounds` instead of `workArea`.
-   [DOCS] Updated README with "Super Tutorial" and visual memes.

---

**Contributors**: @henrkk123
