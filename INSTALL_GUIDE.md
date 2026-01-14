# 🎮 The Ultimate Guide to CV-Overlay Pro

Welcome to the **CV-Overlay Pro** ecosystem. This guide will take you from "Zero" to "Hero" in about 5 minutes.

> **Difficulty**: Beginner 🟢
> **Time**: ~5 Mins ⏱️

---

## 🏗️ Phase 1: The Foundation (Prerequisites)

Before we can run high-end AI, we need the basics.

### 1. Install Python (The Brain)
We need Python 3.10 or newer.
1.  Go to [python.org/downloads](https://www.python.org/downloads/).
2.  **Vital Step for Windows**: Check the box **"Add Python to PATH"** in the installer.
3.  Install it.

### 2. Install Node.js (The Graphics)
We need Node to run the "Liquid Glass" UI.
1.  Go to [nodejs.org](https://nodejs.org/).
2.  Download the **LTS Version** (Recommended).
3.  Install it with default settings.

---

## ⬇️ Phase 2: Setup The Project

### 1. Open the Terminal
*   **Mac**: Press `Cmd + Space`, type "Terminal", hit Enter.
*   **Windows**: Press `Start`, type "cmd", open Command Prompt.

### For Mac 🍎
1.  Open Terminal.
2.  Copy/Paste:
    ```bash
    pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python
    cd overlay-ui && npm install && cd ..
    ```

### For Windows 🪟 (Easiest Way)
1.  **Double-Click** the file named:
    > **`setup_windows.bat`**
2.  Wait for it to say "SETUP COMPLETE".

---

## 🚀 Phase 3: Launch!

You made it. Now let's start the engine.

### For Mac 🍎
simply **Double-Click** the file named:
> **`start_overlay.command`**

### For Windows 🪟
simply **Double-Click** the file named:
> **`start_overlay.bat`**

---

## 🎮 How to Play

1.  **The Overlay**: It will appear as a transparent glass layer over your screen.
2.  **Status**: Look for "VISION ENGINE: ONLINE" in the top corner.
3.  **Combat Mode**: Press **`0` (Zero)** on your keyboard to toggle Aim Assist.
    *   *Green Glow*: Assist Active.
    *   *Red/No Glow*: Passive Mode.

### Pro Tips 💡
*   **Game Mode**: Run your game in **Borderless Window** or **Windowed Fullscreen**. Exclusive Fullscreen might hide the overlay.
*   **Training**: Want to teach it new targets? Run the `train_model` script!

---

## 🆘 Troubleshooting

**"Command not found" error?**
> You didn't add Python or Node to your PATH/Environment Variables during installation. Re-install them and check the boxes!

**Overlay is black?**
> Make sure your game is **NOT** in Exclusive Fullscreen.

**"UI Dependencies not found"?**
> You skipped Phase 2, Step 3 (`npm install`). Go do it!
