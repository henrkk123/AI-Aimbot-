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

    def detect_screen(self, conf_threshold=0.5):
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
        max_conf = 0.0
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                if confidence > max_conf:
                    max_conf = confidence
                    x1, y1, x2, y2 = box.xyxy[0]
                    
                    # Offset local ROI coordinates to Global Screen coordinates
                    global_x1 = int(x1) + self.roi_left
                    global_y1 = int(y1) + self.roi_top
                    global_x2 = int(x2) + self.roi_left
                    global_y2 = int(y2) + self.roi_top
                    
                    w = global_x2 - global_x1
                    h = global_y2 - global_y1
                    
                    # Returns top-left x,y for drawing
                    best_box = (global_x1, global_y1, w, h, confidence)
                    
        return best_box
