<div align="center">

# 🤖 CV-Overlay Pro
### Next-Gen AI Aim Assist & Vision System

![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-blue?style=for-the-badge&logo=react&logoColor=white)
![Electron](https://img.shields.io/badge/Electron-Desktop-purple?style=for-the-badge&logo=electron&logoColor=white)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-red?style=for-the-badge&logo=ultralytics&logoColor=white)

<br />

<!-- VISUAL DEMO -->
<div align="center">
  <img src="https://media1.tenor.com/m/bckhFp1icFYAAAAC/aimbot.gif" width="45%" alt="Aimbot Activated" />
  <img src="https://media1.tenor.com/m/J3SGgrxQeGQAAAAC/gif-ref-do-something.gif" width="45%" alt="Do Something" />
</div>

<br />

**Zero Latency. Liquid Glass UI. GPU Accelerated.**
<br />
A hybrid computer vision overlay designed for high-refresh-rate gaming.
<br />

[**⬇️ Download & Install**](#-quick-start) • [**📚 Documentation**](docs/INSTALL_GUIDE.md) • [**🐛 Report Bug**](../../issues)

</div>

---

## ⚡️ Launch in 1 Click

We built this for speed. No terminal needed after setup.

### 🍎 For macOS
> **Double-click** `start_overlay.command`

### 🪟 For Windows
> **Double-click** `start_overlay.bat`

---

## ✨ Why CV-Overlay Pro?

| Feature | Description |
| :--- | :--- |
| **🚀 Zero-Latency Core** | Python backend runs decoupled on your **GPU** (CUDA/MPS) for instant inference. |
| **💎 Liquid Glass UI** | A stunning, transparent **Electron/React** overlay with 144Hz animations. |
| **🎯 Smart ROI** | Scans only the center 640px zone, boosting FPS by **90%**. |
| **⌨️ Instante Bindings** | Toggle "Combat Mode" instantly with the `0` key via low-level hooks. |

---

## 🔥 Latest Updates (v0.1.19 - Stability Fixes)
-   **🚀 Optimization**: Root folder cleaned up (files moved to `docs/`).
-   **🛠️ Trainer**: Fixed dependency crash.
-   **👻 Ghost Mode**: Self-aim prevention active.
-   **🎯 Sticky Aim**: Target switching fixed.

---

## 🛠️ Quick Start

New to this? Read our **[Step-by-Step Installation Guide](docs/INSTALL_GUIDE.md)** or **[Training Strategy](docs/TRAINING_GUIDE.md)**.

### Prerequisite Check
```bash
python --version   # Should be 3.10+
node -v            # Should be 18+
```

## 🛠️ Quick Start

New to this? Read our **[Step-by-Step Installation Guide](INSTALL_GUIDE.md)**.

### 1. Prerequisites
Ensure you have these installed:
*   [Python 3.10+](https://www.python.org/) (Add to PATH!)
*   [Node.js 18+](https://nodejs.org/)

### 2. Launch
The launcher will **automatically install** all dependencies on the first run.

#### 🍎 Mac / Linux
```bash
./start_overlay.command
```

#### 🪟 Windows
```bat
start_overlay.bat
```
*(Wait a few minutes on first launch for the self-healing system to finish)*

---

## 🎮 Controls

- **`0` (Zero Key)**: Toggle **Combat Mode** (Aim Assist) ON/OFF.
- **`start_overlay`**: Launches the Game Overlay.
- **`train_model`**: Launches the Model Trainer.

---

<div align="center">
  <sub>Built with ❤️ by <b>Henni12</b> using YoloV8 & Electron</sub>
</div>
