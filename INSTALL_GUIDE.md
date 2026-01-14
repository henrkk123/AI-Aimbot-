# 📦 CV-Overlay Installation Guide

Welcome! This guide will help you set up the **CV-Overlay Pro** system from scratch.

---

## 🏗️ 1. Install Prerequisites

Before you begin, ensure you have the following installed on your machine.

### A. Python (The Brain)
-   **Requirement**: Python 3.10 or newer.
-   **Verification**: Open a terminal and type:
    ```bash
    python --version
    ```
-   **Download**: [python.org](https://www.python.org/downloads/)

### B. Node.js (The UI)
-   **Requirement**: Node.js 18.0 or newer.
-   **Verification**:
    ```bash
    node -v
    npm -v
    ```
-   **Download**: [nodejs.org](https://nodejs.org/)

---

## ⚡ 2. Setup the Project

### step 1: Clone or Unzip
If you haven't already, download this folder to your computer.

### step 2: Python Backend Setup
We need to install the AI libraries (YOLO, FastAPI, etc.).

1.  Open your **Terminal** or **Command Prompt** in the project folder.
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv .venv
    ```
3.  Activate it:
    *   **Mac/Linux**: `source .venv/bin/activate`
    *   **Windows**: `.venv\Scripts\activate`
4.  Install dependencies:
    ```bash
    pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python
    ```

### Step 3: UI Frontend Setup
We need to install the liquid-glass interface libraries.

1.  Navigate to the UI folder:
    ```bash
    cd overlay-ui
    ```
2.  Install packages:
    ```bash
    npm install
    ```
3.  Go back to the root:
    ```bash
    cd ..
    ```

---

## 🚀 3. Launching the App

### The Easy Way
-   **Mac**: Double-Click `start_overlay.command`.
-   **Windows**: Double-Click `start_overlay.bat`.

### The Manual Way
If you prefer terminal control:
1.  **Start the Backend**:
    ```bash
    python server.py
    ```
2.  **Start the UI** (New Terminal):
    ```bash
    cd overlay-ui
    npm run electron
    ```

---

## 🛠️ Troubleshooting

-   **"Module Not Found"**: Ensure you activated your `.venv` before running python.
-   **Overlay is Black/Not Transparent**:
    -   *Windows*: Ensure Aero/Transparency effects are enabled in Windows Settings.
    -   *Mac*: Ensure you are not in strict full-screen mode for some apps; windowed modes work best.
-   **"Command not found"**: Ensure Python and Node are added to your system PATH during installation.

**Enjoy your new high-perforamnce overlay!** 🎯
