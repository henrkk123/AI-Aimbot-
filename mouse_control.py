import pyautogui
import math

# Fail-safe
pyautogui.FAILSAFE = True
# CRITICAL FOR GAMING: Remove built-in delays
pyautogui.PAUSE = 0.0

def move_mouse_to(target_x, target_y, smooth_factor=0.5):
    """
    Moves the mouse towards the target (x, y).
    """
    current_x, current_y = pyautogui.position()
    
    dx = target_x - current_x
    dy = target_y - current_y
    
    new_x = current_x + (dx * smooth_factor)
    new_y = current_y + (dy * smooth_factor)
    
    # Instant move commands for gaming
    pyautogui.moveTo(new_x, new_y, duration=0, _pause=False)

def click_mouse():
    pyautogui.click(_pause=False)
