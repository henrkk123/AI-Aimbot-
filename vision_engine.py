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
        self.conf_threshold = 0.50 
        self.sticky_radius = 250    
        self.target_offset = 0.0    # -0.5 (Top) to 0.5 (Bottom)

        
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

        # 2. Setup ROI (Region of Interest) - Center Crop
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[1] # Primary monitor
            screen_w = monitor["width"]
            screen_h = monitor["height"]
            self.roi_left = monitor["left"] + (screen_w - roi_size) // 2
            self.roi_top = monitor["top"] + (screen_h - roi_size) // 2

        print(f"🎯 Vision ROI Set: {roi_size}x{roi_size} at ({self.roi_left}, {self.roi_top})")
        
        # 3. Screen Capture Setup (DXCam for Windows, MSS fallback)
        self.camera = None
        self.use_dxcam = False
        if sys.platform == "win32":
            try:
                import dxcam
                self.camera = dxcam.create(region=(self.roi_left, self.roi_top, self.roi_left + roi_size, self.roi_top + roi_size))
                self.use_dxcam = True
                print("🚀 VISION: DXCam (DirectX) Capture - ENABLED")
            except Exception as e:
                print(f"⚠️ VISION: DXCam failed ({e}), falling back to MSS")
        
        if not self.use_dxcam:
            import mss
            self.sct = mss.mss()
            self.capture_area = {
                "top": self.roi_top,
                "left": self.roi_left,
                "width": roi_size,
                "height": roi_size
            }
            print("🕒 VISION: MSS Capture - ENABLED")

        self.lock = threading.Lock()
        
        # Tracking Memory for Sticky Logic
        self.last_target_center = None
        
    def capture_screen(self):
        """
        Captures the defined ROI using the fastest available method.
        """
        if self.use_dxcam:
            frame = self.camera.grab()
            if frame is not None:
                # DXCam returns RGB by default, often as a numpy array
                return frame
            # If grab fails, it returns None
        
        # Fallback to MSS
        screenshot = self.sct.grab(self.capture_area)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB) # Keep RGB for YOLO

    def detect_screen(self, conf_threshold=None):
        """
        Captures screen ROI and runs inference. 
        Returns tuple: (x, y, w, h, conf) in GLOBAL coordinates.
        """
        if conf_threshold is None:
            conf_threshold = self.conf_threshold

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
                
                # Apply Target Offset (Shift Vertical Center)
                cy += int(h * self.target_offset)

                
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
                    if dist < self.sticky_radius: # Dynamic Sticky Radius
                        score += 0.5 # MASSIVE BONUS to keep lock
                
                if score > max_score:
                    max_score = score
                    best_box = (global_x1, global_y1, w, h, confidence)
                    best_center = (cx, cy)
        
        # Update memory
        self.last_target_center = best_center
                    
        return best_box
