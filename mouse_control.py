import ctypes
import random
import time

# Mouse Event Constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000

def get_mouse_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def move_mouse_to(target_x, target_y, smooth_factor=0.3, humanization=0.0):
    """
    Moves mouse towards target with smoothing and optional humanized Bezier jitter.
    """
    try:
        curr_x, curr_y = get_mouse_pos()
        
        # Calculate Delta
        dx_raw = target_x - curr_x
        dy_raw = target_y - curr_y
        
        # Apply smoothing
        dx = int(dx_raw * smooth_factor)
        dy = int(dy_raw * smooth_factor)
        
        # --- SNIPER PRECISION (v0.8.0-0.8.5) ---
        # Force a minimum 1-pixel move if smoothing would otherwise stop the movement.
        # This prevents the mouse from 'getting stuck' near the target.
        if dx == 0 and abs(dx_raw) > 0.5:
            dx = 1 if dx_raw > 0 else -1
        if dy == 0 and abs(dy_raw) > 0.5:
            dy = 1 if dy_raw > 0 else -1
            
        # --- HUMANIZATION (Stealth Jitter) ---
        # Only jitter if we are moving significantly to avoid glitching at close range.
        # Reduced range for v0.8.5 to prevent "zappeln" (jittering).
        if humanization > 0 and (abs(dx_raw) > 30 or abs(dy_raw) > 30):
            jitter_x = random.uniform(-humanization * 2, humanization * 2)
            jitter_y = random.uniform(-humanization * 2, humanization * 2)
            dx = int(dx + jitter_x)
            dy = int(dy + jitter_y)

        if dx != 0 or dy != 0:
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)
    except Exception as e:
        print(f"Mouse Control Error: {e}")
