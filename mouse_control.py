import pyautogui
import math

# Fail-safe: moving mouse to corner will throw exception
pyautogui.FAILSAFE = True

def move_mouse_to(target_x, target_y, smooth_factor=0.5):
    """
    Moves the mouse towards the target (x, y).
    smooth_factor: 0.0 to 1.0 (1.0 = instant, 0.1 = very slow/smooth)
    """
    current_x, current_y = pyautogui.position()
    
    # Calculate vector to target
    dx = target_x - current_x
    dy = target_y - current_y
    
    # Simple smoothing: move a percentage of the way there
    new_x = current_x + (dx * smooth_factor)
    new_y = current_y + (dy * smooth_factor)
    
    # Move
    pyautogui.moveTo(new_x, new_y)

def click_mouse():
    pyautogui.click()
