import asyncio
import threading
import json
import time
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import existing logic
# ensuring we can import from local directory
import sys
import os
sys.path.append(os.getcwd())

try:
    from vision_engine import VisionEngine
    from mouse_control import move_mouse_to
    from input_listener import GlobalInputListener
except ImportError:
    print("Project files not found. Make sure you are in the root directory.")

app = FastAPI()

# Allow CORS for development (React runs on localhost:5173, FastApi on 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
class GameState:
    def __init__(self):
        self.latest_detection = None
        self.running = True
        self.combat_mode = False
        self.vision = None

state = GameState()

# Toggle Callback
def on_hotkey_toggle():
    state.combat_mode = not state.combat_mode
    status = "ON" if state.combat_mode else "OFF"
    print(f"🔄 COMBAT MODE: {status}")

# Start Listener
listener = GlobalInputListener(on_hotkey_toggle)
listener.start()

def vision_loop():
    """Runs the YOLO detection in a separate thread (High Freq)."""
    print("👁️ VISION ENGINE STARTED")
    try:
        # Initialize Engine (it will auto-select GPU)
        state.vision = VisionEngine(roi_size=640)
        
        while state.running:
            # 1. Detect
            target = state.vision.detect_screen()
            state.latest_detection = target
            
            # 2. Combat Logic (server-side for lowest latency)
            if state.combat_mode and target:
                x, y, w, h, conf = target
                # Basic center calculation
                cx = x + w // 2
                cy = y + h // 2
                
                # Move mouse (optional, can be toggled)
                try:
                    move_mouse_to(cx, cy)
                except:
                    pass
                    
            # Yield slightly to prevent 100% CPU lock if VSync is off
            time.sleep(0.001) 
            
    except Exception as e:
        print(f"❌ Vision Loop Error: {e}")

# Start Vision Thread on Load
threading.Thread(target=vision_loop, daemon=True).start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ UI CONNECTED")
    try:
        while True:
            # Prepare Payload
            data = {
                "detected": False,
                "combat_enabled": state.combat_mode
            }
            
            target = state.latest_detection
            if target:
                x, y, w, h, conf = target
                data.update({
                    "detected": True,
                    "x": x, "y": y, "w": w, "h": h, 
                    "cx": x + w//2, "cy": y + h//2,
                    "conf": float(conf)
                })
            
            # Send to UI
            await websocket.send_text(json.dumps(data))
            
            # Receive commands? (Non-blocking check)
            # WebSockets in FastAPI are usually bidirectional but for a strict loop
            # we might want to use a separate task or just polling.
            # ideally we just push data here.
            
            # Rate limit UI updates to ~60 FPS (16ms)
            # The vision loop runs faster (e.g. 144Hz), but UI doesn't need to redraw that fast.
            await asyncio.sleep(0.016)
            
    except Exception as e:
        print(f"🔌 UI Disconnected: {e}")

@app.post("/toggle_combat")
def toggle_combat():
    state.combat_mode = not state.combat_mode
    return {"status": "ok", "combat_mode": state.combat_mode}

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
