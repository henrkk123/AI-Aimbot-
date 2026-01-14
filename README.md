# 🤖 CV-Overlay: High-Performance AI Aim Assist

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![React](https://img.shields.io/badge/React-19-blue)
![Electron](https://img.shields.io/badge/Electron-Desktop-purple)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-red)

A next-generation, hybrid computer vision overlay designed for high-refresh-rate gaming. It combines a lightweight Python/YOLOv8 backend for zero-latency inference with a modern Electron/React frontend for a stunning "Liquid Glass" visual experience.

## ✨ Features

-   **🚀 Zero-Latency Vision Engine**: Decoupled Python backend running YOLOv8 on your GPU (NVIDIA CUDA / Mac MPS).
-   **🎯 Intelligent ROI Scanning**: Dynamically focuses on the center screen (640x640) for 90% performance gains.
-   **💎 Liquid Glass UI**: A beautiful, transparent, and completely click-through overlay built with React & Framer Motion.
-   **⌨️ Global Hotkeys**: Press `0` to toggle Combat Mode (Aim Assist) instantly.
-   **🕸️ WebSocket Architecture**: 60 FPS smooth UI updates with 144Hz+ logic tick rate.

## 🛠️ Installation

> **New to this?** Check out our detailed [**Beginner Installation Guide**](INSTALL_GUIDE.md) for step-by-step setup instructions.

### Prerequisites
-   **Python 3.10+** (Create a virtual environment recommended)
-   **Node.js 18+**

### Quick Setup

1.  **Install Python Dependencies**:
    ```bash
    pip install ultralytics fastapi uvicorn[standard] websockets pynput pyautogui mss opencv-python
    ```

2.  **Install Node Dependencies**:
    ```bash
    cd overlay-ui
    npm install
    cd ..
    ```

## 🎮 Usage

### One-Click Launch (Recommended)

**Mac / Linux**:
 Double-click `start_overlay.command` or run:
```bash
./start_overlay.command
```

**Windows**:
Double-click `start_overlay.bat`.

### Manual Controls
-   **`0` (Zero)**: Toggle Aim Assist ("Combat Mode").
-   **Training**: Run `python gui_training.py` to open the Dataset Management & Training tool.

## 📂 Project Structure

-   `/server.py` - The Brain. specific optimization logic for mouse movement and vision.
-   `/vision_engine.py` - GPU-accelerated Screen Capture & Inference.
-   `/overlay-ui/` - React/Electron Source Code.
-   `/gui_training.py` - Standalone utility for training custom YOLO models.

---

**Disclaimer**: This software is for educational and research purposes only. Use responsibly in online games.
