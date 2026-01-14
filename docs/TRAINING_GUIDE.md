# 🧠 Training Guide for CV-Overlay Pro

> **"Data is king. The model is just the student."**

If your aimbot misses, it's not the code's fault. It's the training data.
Here is exactly how many images you need.

## 📊 The "How Many?" Rule

| Number of Images | Intelligence Level | Behavior |
| :--- | :--- | :--- |
| **100 - 300** | 👶 Toddler | Locks onto walls, confused by shadows. Fun to test, bad to play. |
| **500 - 1,000** | 🎓 Student | Reliable in training maps (white walls). Misses in complex cities. |
| **1,000 - 3,000** | 🔫 **Soldier (Recommended)** | Hits 90% of shots. Can handle different backgrounds. |
| **5,000 - 10,000+** | 🤖 **AI God (Spinbot)** | Inhuman. Can see heads pixels away. Ignoring bushes/smoke. |

## 🎨 Quality > Quantity

A "Dataset" is a folder of Screenshots + Text Files (labels).

### ❌ MISTAKE #1: Only One Map
If you only take screenshots in "Creative Mode" (clean walls), the bot thinks **Enemies only exist near clean walls**.
*   **Result**: In Battle Royale (trees, grass), it goes blind.
*   **Fix**: Take screenshots in Grass, Snow, City, and Night.

### ❌ MISTAKE #2: Only One Distance
If all your pictures are close-up...
*   **Result**: It won't shoot snipers 200m away.
*   **Fix**: 50% Close Combat, 50% Long Range.

## 🚀 Performance Myths

**"If I train with 10,000 images, will the bot be slower?"**
> **NO.**
> The `.pt` file (brain) is ALWAYS the same size (~6MB for YOLOv8n).
> 100 images = 6MB dumb brain.
> 10,000 images = 6MB smart brain.
> **Speed (FPS) is identical.**

**"How long does training take?"**
> On your RTX 5070:
> *   500 Images: ~2 minutes.
> *   5,000 Images: ~15-20 minutes.
> It's incredibly fast.

---

## 🛠️ Workflow

1.  Play the game. Record video or spam Screenshots.
2.  Use a label tool (like `Roboflow` or `LabelImg`) to draw boxes around enemies.
3.  Export as **YOLOv8 Format** (txt files).
4.  Put them in a folder.
5.  Open `gui_training.py` -> Select Folder -> **TRAIN**.

Happy Grinding. 🎯
