import ctypes
import os

# Windows User32 API Constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000

def move_mouse_to(target_x, target_y, smooth_factor=0.5):
    """
    Moves the mouse RELATIVE to current position locally.
    This works in FPS games where 'cursor' is locked to center.
    """
    try:
        # 1. Get current position (Screen coordinates)
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        
        # 2. Calculate Delta (Distance to target)
        dx = int((target_x - pt.x) * smooth_factor)
        dy = int((target_y - pt.y) * smooth_factor)
        
        # 3. Send Hardware Input (Relative Move)
        # This bypasses windows pointer ballistics and works in Raw Input games
        if dx != 0 or dy != 0:
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)
            
    except Exception as e:
        print(f"Mouse Error: {e}")

def click_mouse():
    # Standard Click (often works, but we can upgrade to ctypes if needed)
    # MOUSEEVENTF_LEFTDOWN = 0x0002
    # MOUSEEVENTF_LEFTUP = 0x0004
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0) # Down
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0) # Up
