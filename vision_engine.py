from ultralytics import YOLO
import mss
import numpy as np
import cv2
import threading

class VisionEngine:
    def __init__(self, model_path='yolov8n.pt', roi_size=640):
        """
        Initializes the YOLOv8 model and screen capture with GPU acceleration.
        roi_size: Size of the square box to capture at the center of the screen.
        """
        self.roi_size = roi_size
        
        # 1. Hardware Acceleration Selection
        import torch
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = 0 # GPU 0
            device_name = torch.cuda.get_device_name(0)
            print(f"🚀 FITTING: NVIDIA GPU DETECTED [{device_name}] - ENABLED")
        elif torch.backends.mps.is_available():
            self.device = 'mps'
            print("🚀 FITTING: APPLE SILICON GPU (MPS) - ENABLED")
        else:
            print("⚠️ WARNING: NO GPU DETECTED. RUNNING ON CPU (MAY BE SLOW).")

        print(f"Loading YOLO model: {model_path} to {self.device}...")
        self.model = YOLO(model_path)
        
        # Force model to device immediately
        self.model.to(self.device)

        self.sct = mss.mss()
        
        # Setup ROI (Region of Interest) - Center Crop
        monitor = self.sct.monitors[1] # Primary monitor
        screen_w = monitor["width"]
        screen_h = monitor["height"]
        
        self.roi_left = monitor["left"] + (screen_w - roi_size) // 2
        self.roi_top = monitor["top"] + (screen_h - roi_size) // 2
        
        self.capture_area = {
            "top": self.roi_top,
            "left": self.roi_left,
            "width": roi_size,
            "height": roi_size
        }
        
        print(f"🎯 Vision ROI Set: {roi_size}x{roi_size} at ({self.roi_left}, {self.roi_top})")
        self.lock = threading.Lock()
        
        # Tracking Memory for Sticky Logic
        self.last_target_center = None
        
    def capture_screen(self):
        """
        Captures the defined ROI.
        """
        # Capture strictly the ROI
        screenshot = self.sct.grab(self.capture_area)
        
        # Convert to numpy array
        img = np.array(screenshot)
        
        # Drop alpha channel (BGRA -> BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img

    def detect_screen(self, conf_threshold=0.30): # Lowered base threshold to catch fast movers
        """
        Captures screen ROI and runs inference. 
        Returns tuple: (x, y, w, h, conf) in GLOBAL coordinates.
        """
        frame = self.capture_screen()
        
        # Run inference on the specific device
        # 'half=True' uses FP16 precision (faster on GPU)
        # 'verbose=False' keeps terminal clean
        results = self.model(frame, stream=True, verbose=False, conf=conf_threshold, device=self.device)
        # Note: half=True is automatic on many recent YOLO versions when on GPU, 
        # but we let ultralytics handle the defaults for stability unless explicit speedup is needed.
        
        best_box = None
        max_score = 0.0
        best_center = None
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                
                # Get Coords
                x1, y1, x2, y2 = box.xyxy[0]
                global_x1 = int(x1) + self.roi_left
                global_y1 = int(y1) + self.roi_top
                global_x2 = int(x2) + self.roi_left
                global_y2 = int(y2) + self.roi_top
                
                w = global_x2 - global_x1
                h = global_y2 - global_y1
                
                # Center
                cx = global_x1 + w // 2
                cy = global_y1 + h // 2
                
                # --- PLAYER DEADZONE FILTER ---
                # Fortnite/3rd Person: Player is Bottom Center.
                # ROI is 640x640. Center is 320,320.
                # Rel Y > 320 (Bottom half) AND Rel X within 100px of center.
                
                rel_x = cx - self.roi_left
                rel_y = cy - self.roi_top
                
                # Config: Bottom 55% height, Center 10% width (More lenient)
                if rel_y > (self.roi_size * 0.55): 
                     if abs(rel_x - (self.roi_size / 2)) < (self.roi_size * 0.10): # Shrink width check to 10%
                         # print("👻 Ignored Player")
                         continue 
                
                # Score = Conf + Sticky Bonus
                score = confidence
                if self.last_target_center:
                    lcx, lcy = self.last_target_center
                    dist = np.hypot(cx - lcx, cy - lcy)
                    if dist < 100: # 100px Sticky Radius
                        score += 0.3 # BIG BONUS to keep lock
                
                if score > max_score:
                    max_score = score
                    best_box = (global_x1, global_y1, w, h, confidence)
                    best_center = (cx, cy)
        
        # Update memory
        self.last_target_center = best_center
                    
        return best_box
