import customtkinter as ctk
import tkinter as tk
from data_simulation import generate_dummy_data, calculate_centroid
from gui_training import TrainingWindow
import sys
import platform
import random
import threading

class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- VISION ENGINE SETUP ---
        try:
            from vision_engine import VisionEngine
            self.vision = VisionEngine() # Load YOLO
            self.use_vision = True
        except Exception as e:
            print(f"Error loading VisionEngine: {e}")
            self.use_vision = False

        # Window setup
        self.title("Computer Vision Overlay")
        
        # Gets the requested values of the height and width.
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Position right in the middle of the screen
        self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        
        # Make it transparent and topmost
        self.wm_attributes("-topmost", True)
        
        # Platform specific transparency
        self.current_os = platform.system()
        if self.current_os == "Windows":
            self.lift()
            self.wm_attributes("-transparentcolor", "black")
            self.config(bg="black")
            self.transparent_color = "black"
        elif self.current_os == "Darwin":  # macOS
            try:
                self.wm_attributes("-transparent", True)
                self.config(bg="systemTransparent")
                self.transparent_color = "systemTransparent"
            except Exception:
                print("Warning: macOS transparency setup failed or limited.")
                self.attributes("-alpha", 0.5)
                self.transparent_color = "black" # Fallback
        else:
            self.attributes("-alpha", 0.7)
            self.transparent_color = "black"

        self.attributes('-fullscreen', True)
        
        # Create a Canvas for drawing
        self.canvas = ctk.CTkCanvas(self, width=self.screen_width, height=self.screen_height, 
                                    bg=self.transparent_color, 
                                    highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Input listener
        self.bind("<q>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())
        
        # --- UI CONTROLS ---
        # Floating Control Panel (Top Left)
        self.control_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10, border_width=1, border_color="#00ff00")
        self.control_frame.place(relx=0.02, rely=0.05, anchor="nw")
        
        self.title_label = ctk.CTkLabel(self.control_frame, text="YOLO SYSTEM ONLINE", text_color="#00ff00", font=("Orbitron", 14, "bold"))
        self.title_label.pack(padx=10, pady=(10, 5))
        
        self.train_ui_btn = ctk.CTkButton(self.control_frame, text="OPEN DATASET UI", command=self.open_training_ui,
                                          fg_color="#003300", hover_color="#005500", text_color="#00ff00", border_color="#00ff00", border_width=1)
        self.train_ui_btn.pack(padx=10, pady=5)
        
        # Mouse Control Switch (HOTKEY: 0)
        self.mouse_control_var = ctk.BooleanVar(value=False)
        self.mouse_switch = ctk.CTkSwitch(self.control_frame, text="COMBAT MODE [0]", variable=self.mouse_control_var,
                                          progress_color="#ff0000", button_color="#cc0000", button_hover_color="#ff3333",
                                          text_color="#ff0000", font=("Arial", 10, "bold"))
        self.mouse_switch.pack(padx=10, pady=(5, 10))
        
        # State
        self.training_window = None
        
        # Input Listener (Global Hotkeys)
        try:
            from input_listener import GlobalInputListener
            self.listener = GlobalInputListener(self.toggle_combat_mode)
            self.listener.start()
        except Exception as e:
            print(f"Error starting hotkey listener: {e}")

        # Threading for Vision (Max FPS)
        self.latest_detection = None
        self.vision_thread_running = True
        
        if self.use_vision:
            # Start vision in a separate thread
            self.vision_thread = threading.Thread(target=self.vision_loop, daemon=True)
            self.vision_thread.start()
            
            # Print GPU Info if available (YOLO usually prints this, but let's be explicit)
            try:
                import torch
                if torch.cuda.is_available():
                    print(f"✅ HIGH-PERFORMANCE MODE: GPU DETECTED: {torch.cuda.get_device_name(0)}")
                elif torch.backends.mps.is_available():
                    print("✅ HIGH-PERFORMANCE MODE: APPLE SILICON (MPS) DETECTED")
                else:
                    print("⚠️ STANDARD MODE: CPU ONLY (May be slower)")
            except:
                pass

        # Start the update loop (UI)
        self.update_overlay()

    def vision_loop(self):
        """Runs inference as fast as possible in background."""
        while self.vision_thread_running:
            try:
                # This blocks only as long as inference takes
                result = self.vision.detect_screen()
                self.latest_detection = result
            except Exception as e:
                print(f"Vision Loop Error: {e}")

    def open_training_ui(self):
        if self.training_window is None or not self.training_window.winfo_exists():
            self.training_window = TrainingWindow(self)
        else:
            self.training_window.focus()

    def draw_bracket(self, x, y, w, h, length=20, color="#00ff00", thickness=3):
        """Draws sci-fi corner brackets properly."""
        # Top Left
        self.canvas.create_line(x, y, x + length, y, fill=color, width=thickness)
        self.canvas.create_line(x, y, x, y + length, fill=color, width=thickness)
        # Top Right
        self.canvas.create_line(x + w, y, x + w - length, y, fill=color, width=thickness)
        self.canvas.create_line(x + w, y, x + w, y + length, fill=color, width=thickness)
        # Bottom Left
        self.canvas.create_line(x, y + h, x + length, y + h, fill=color, width=thickness)
        self.canvas.create_line(x, y + h, x, y + h - length, fill=color, width=thickness)
        # Bottom Right
        self.canvas.create_line(x + w, y + h, x + w - length, y + h, fill=color, width=thickness)
        self.canvas.create_line(x + w, y + h, x + w, y + h - length, fill=color, width=thickness)

    def draw_hud_elements(self, cx, cy):
        """Draws decorative HUD lines"""
        # Crosshair lines
        self.canvas.create_line(cx - 30, cy, cx - 10, cy, fill="#00ff00", width=1)
        self.canvas.create_line(cx + 10, cy, cx + 30, cy, fill="#00ff00", width=1)
        self.canvas.create_line(cx, cy - 30, cx, cy - 10, fill="#00ff00", width=1)
        self.canvas.create_line(cx, cy + 10, cx, cy + 30, fill="#00ff00", width=1)

    def update_overlay(self):
        """
        Main loop to update the visualization.
        """
        # Clear previous drawings
        self.canvas.delete("all")

        x, y, box_w, box_h = 0, 0, 0, 0
        detected = False
        confidence = 0.0

        if self.use_vision:
            # 1. READ latest result from thread (Instant, no waiting)
            target = self.latest_detection
            if target:
                x, y, box_w, box_h, confidence = target
                detected = True
        else:
            # Fallback to simulation
            w = self.winfo_width()
            h = self.winfo_height()
            if w < 100: w = self.screen_width
            if h < 100: h = self.screen_height
            x, y, box_w, box_h = generate_dummy_data(w, h)
            detected = True
            confidence = random.uniform(0.8, 0.99)

        if detected:
            # 2. Math: Calculate Centroid
            cx, cy = calculate_centroid(x, y, box_w, box_h)
            
            # 3. Visualization (Sci-Fi Style)
            # HUD Brackets
            self.draw_bracket(x, y, box_w, box_h, length=min(box_w, box_h)//4, color="#00ff00")
            
            # Center target
            self.draw_hud_elements(cx, cy)
            self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="red", outline="#00ff00")
            
            # Text Info
            self.canvas.create_text(x + box_w + 5, y, text="TARGET LOCKED", fill="#00ff00", anchor="nw", font=("Courier", 12, "bold"))
            self.canvas.create_text(x + box_w + 5, y + 15, text=f"CONF: {confidence:.2%}", fill="#00ff00", anchor="nw", font=("Courier", 10))
            self.canvas.create_text(x + box_w + 5, y + 30, text=f"MODEL: YOLOv8n", fill="#00ff00", anchor="nw", font=("Courier", 10))

            # 4. Combat Logic (Mouse Control / Aim Assist Only)
        if self.mouse_control_var.get():
            try:
                from mouse_control import move_mouse_to
                # Aimbot
                move_mouse_to(cx, cy, smooth_factor=0.3)
                
                # Visual indicator
                self.canvas.create_text(self.screen_width/2, 50, text="!!! AIM ASSIST ACTIVE !!!", fill="red", font=("Arial", 16, "bold"))
                
                # No Triggerbot (removed per request)
                    
            except Exception as e:
                print(f"Mouse control error: {e}")
        
        # Schedule next update
        # 10ms delay implies target ~100 FPS, but inference will bottle neck it.
        # This is async in Tkinter so it waits for prev call to finish mostly.
        self.after(10, self.update_overlay)

    def toggle_combat_mode(self):
        """Toggles the Aim Assist switch."""
        current = self.mouse_control_var.get()
        self.mouse_control_var.set(not current)
        state = "ENABLED" if not current else "DISABLED"
        print(f"Combat Mode {state}")
