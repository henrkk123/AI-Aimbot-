# 🧠 Training Guide for CV-Overlay Pro

> **"Data is king. The model is just the student."**

If your aimbot misses, it's not the code's fault. It's the training data.

---

## 📊 The "How Many?" Rule

| Quantity | Intelligence Level | Behavior |
| :--- | :--- | :--- |
| **100 - 300** | 👶 Toddler | Locks onto walls. Fun test, bad for ranked. |
| **1,000 - 3,000** | 🔫 **Soldier (Recommended)** | Reliable. Handles trees, skins, and shadows. |
| **5,000+** | 🤖 **AI God** | Inhuman. Sees pixels you can't see. |

---

## 🌪️ Advanced Feature: The Dataset Mixer (New in v0.1.22)

You don't need one giant folder anymore. You can "mix" datasets.

**Scenario**: 
You have `Folder_A` (Daytime) and `Folder_B` (Nighttime).

1.  Open **`train_model.bat`**.
2.  Click **[+ Add Folder]** -> Select `Folder_A`.
3.  Click **[+ Add Folder]** -> Select `Folder_B`.
4.  Click **START TRAINING**.
    *   *Magic:* The AI automatically copies all images into a temporary Mega-Dataset and trains on everything at once.

---

## 🐁 Mouse Control Settings (Tuning)

The code performs a "Relative Move". Adjust `smooth_factor` in code if needed.
*   **0.5 (Default)**: Balanced. Human-like snap.
*   **0.2**: Very smooth, "Legit" looking.
*   **0.8**: Rage mode. Instant snap.

---

## 🎨 Data Strategy Checklist

- [ ] **Map Variety**: Don't just train in Creative. Go to the Snow biome. Go to the City.
- [ ] **Distance**: Take screenshots close up (Shotgun range) and far away (Sniper range).
- [ ] **Lighting**: Day, Night, Sunset. Shadows change everything for an AI.

**Pro Tip**: If the bot ignores a specific skin (e.g., Banana Guy), take 50 screenshots of just that skin and add it to the mixer. It will learn instantly.
