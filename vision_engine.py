from ultralytics import YOLO
import mss
import numpy as np
import cv2
import threading

class VisionEngine:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initializes the YOLOv8 model and screen capture.
        """
        print(f"Loading YOLO model: {model_path}...")
        self.model = YOLO(model_path)
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1] # Primary monitor
        self.lock = threading.Lock()
        
    def capture_screen(self):
        """
        Captures the screen and converts it to a format YOLO likes (BGR/RGB).
        """
        # Capture strictly the monitor area
        # MSS returns BGRA, OpenCV needs BGR for default behavior, 
        # but YOLO can handle multiple formats. We'll stick to BGR for consistency if we use cv2.
        screenshot = self.sct.grab(self.monitor)
        
        # Convert to numpy array
        img = np.array(screenshot)
        
        # Drop alpha channel (BGRA -> BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img

    def detect_screen(self, conf_threshold=0.5):
        """
        Captures screen and runs inference. 
        Returns tuple: (x, y, w, h) of the BEST detection (highest confidence), or None.
        """
        frame = self.capture_screen()
        
        # Run inference
        # stream=True is faster but returns a generator
        results = self.model(frame, stream=True, verbose=False, conf=conf_threshold)
        
        best_box = None
        max_conf = 0.0
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                if confidence > max_conf:
                    max_conf = confidence
                    # Box format: xywh (center_x, center_y, width, height) is standard YOLO, 
                    # but check if we get xyxy. r.boxes.xywh returns center_x, center_y, w, h.
                    # We usually want top-left x,y for drawing.
                    # Let's get xyxy -> top-left x, y, bottom-right x, y
                    x1, y1, x2, y2 = box.xyxy[0]
                    
                    x = int(x1)
                    y = int(y1)
                    w = int(x2 - x1)
                    h = int(y2 - y1)
                    
                    best_box = (x, y, w, h, confidence)
                    
        return best_box
