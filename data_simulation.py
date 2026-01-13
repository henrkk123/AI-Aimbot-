import random

def generate_dummy_data(screen_width, screen_height):
    """
    Generates a dummy bounding box (x, y, width, height).
    Simulates simple movement by picking a random spot, 
    but for a smoother look in a real app, one might use a random walk.
    Here we just return a valid random box.
    """
    # Box size
    w = random.randint(50, 200)
    h = random.randint(50, 200)
    
    # Position (ensure it stays within screen bounds)
    max_x = screen_width - w
    max_y = screen_height - h
    
    x = random.randint(0, max(0, max_x))
    y = random.randint(0, max(0, max_y))
    
    return x, y, w, h

def calculate_centroid(x, y, w, h):
    """
    Calculates the center (cx, cy) of the bounding box.
    """
    cx = x + (w / 2)
    cy = y + (h / 2)
    return cx, cy
