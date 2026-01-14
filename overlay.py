import customtkinter as ctk
import tkinter as tk
from data_simulation import generate_dummy_data, calculate_centroid
from gui_training import TrainingWindow
import sys
import platform
import random
import threading
import json
import os
import ctypes
from ctypes import windll

# Windows Constants for Click-Through
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20

class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIG SETUP ---
        self.config_path = "config.json"
        self.load_config()

        # --- PERFORMANCE TRACKING ---
        import time
        self.last_update_time = time.time()
        self.fps_list = []
        self.inference_latency = 0.0

        # --- VISION ENGINE SETUP ---
        try:
            from vision_engine import VisionEngine
            self.vision = VisionEngine() # Load YOLO
            self.vision.conf_threshold = self.conf_threshold.get()
            self.vision.sticky_radius = self.magnet_radius.get()
            self.use_vision = True
            self.engine_status = "ACTIVE"
        except Exception as e:
            print(f"Error loading VisionEngine: {e}")
            self.use_vision = False
            self.engine_status = "ERROR: VISION CORE FAILED"
            self.engine_error = str(e)

        # Window setup
        self.title("Neural Edge Overlay")
        
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
        # HUD State
        self.hud_minimized = False
        
        # Floating Control Panel (Top Left)
        self.control_frame = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=15, border_width=2, border_color="#00ff00")
        self.control_frame.place(relx=0.02, rely=0.05, anchor="nw")
        
        # Title & Minimize Button HP
        self.header_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.title_label = ctk.CTkLabel(self.header_frame, text="AXION CORE ENGINE", text_color="#00ff00", font=("Orbitron", 14, "bold"))
        self.title_label.pack(side="left", padx=5)
        
        self.minimize_btn = ctk.CTkButton(self.header_frame, text="_", width=25, height=25,
                                           fg_color="#1a1a1a", hover_color="#333", text_color="#00ff00",
                                           command=self.toggle_hud)
        self.minimize_btn.pack(side="right", padx=5)
        
        # Sub-container for hideable elements
        self.menu_container = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.menu_container.pack(fill="x", padx=5)

        self.switch_frame = ctk.CTkFrame(self.menu_container, fg_color="transparent")
        self.switch_frame.pack(fill="x", padx=10)

        self.mouse_switch = ctk.CTkSwitch(self.switch_frame, text="MAGNET LOCK [0]", variable=self.mouse_control_var,
                                          progress_color="#00ff00", button_color="#008800", button_hover_color="#00aa00",
                                          text_color="#00ff00", font=("Orbitron", 11, "bold"))
        self.mouse_switch.pack(side="left", padx=5, pady=10)
        
        # FOV Toggle
        self.fov_switch = ctk.CTkSwitch(self.switch_frame, text="FOV RING", variable=self.show_fov,
                                         progress_color="#00ff00", button_color="#008800",
                                         text_color="#00ff00", font=("Orbitron", 11, "bold"))
        self.fov_switch.pack(side="left", padx=5, pady=10)

        self.settings_btn = ctk.CTkButton(self.menu_container, text="⚙️ SETTINGS", width=100,
                                          fg_color="#1a1a1a", hover_color="#2a2a2a", text_color="#00ff00",
                                          command=self.toggle_settings)
        self.settings_btn.pack(padx=15, pady=5)

        # Expandable Settings Frame
        self.settings_visible = False
        self.settings_frame = ctk.CTkFrame(self.menu_container, fg_color="#141414", corner_radius=10)
        
        # Sliders Organized into Groups
        # --- COMBAT GROUP ---
        self.create_group_label("--- AIMBOT & MOVEMENT ---")
        self.create_slider("Smoothing (Long)", self.smooth_factor, 0.01, 1.0)
        self.create_slider("Magnet Smooth (Snap)", self.magnet_smooth, 0.01, 1.0)
        self.create_slider("Magnet Radius (px)", self.magnet_radius, 10, 500)
        self.create_slider("Target Offset", self.target_offset, -0.5, 0.5)
        self.create_slider("Humanization", self.humanization, 0.0, 1.0)
        
        # --- VISION GROUP ---
        self.create_group_label("--- VISION CORE ---")
        self.create_slider("Conf Threshold", self.conf_threshold, 0.1, 1.0)
        self.create_slider("Predict Intensity", self.prediction_factor, 0.0, 5.0)
        self.create_slider("Lock Stability", self.lock_stability, 0.0, 1.0)
        
        # --- MASK GROUP ---
        self.create_group_label("--- SMART MASK ---")
        self.create_slider("Mask Width", self.mask_width, 0.0, 0.5)
        self.create_slider("Mask Height", self.mask_height, 0.0, 0.8)
        self.create_slider("Mask X Shift", self.mask_x_offset, -1.0, 1.0)
        self.create_slider("Mask Y Shift", self.mask_y_offset, -1.0, 1.0)

        self.train_ui_btn = ctk.CTkButton(self.menu_container, text="NEURAL TRAINING", command=self.open_training_ui,
                                          fg_color="#002200", hover_color="#004400", text_color="#00ff00", border_color="#00ff00", border_width=1)
        self.train_ui_btn.pack(padx=15, pady=(10, 15))
        
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
            
            # Print GPU Info
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

    def load_config(self):
        # Default values
        defaults = {
            "smooth_factor": 0.3,
            "magnet_smooth": 0.8,
            "magnet_radius": 50,
            "conf_threshold": 0.5,
            "prediction_factor": 1.0, # New Prediction setting
            "humanization": 0.2,     # v0.4.0
            "lock_stability": 0.5,   # v0.4.0
            "mask_width": 0.0,
            "mask_height": 0.0,
            "mask_x_offset": 0.0,
            "mask_y_offset": 0.5,
            "combat_mode": False
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    defaults.update(data)
            except: pass

        self.smooth_factor = ctk.DoubleVar(value=defaults["smooth_factor"])
        self.magnet_smooth = ctk.DoubleVar(value=defaults["magnet_smooth"])
        self.magnet_radius = ctk.DoubleVar(value=defaults["magnet_radius"])
        self.conf_threshold = ctk.DoubleVar(value=defaults["conf_threshold"])
        self.target_offset = ctk.DoubleVar(value=defaults["target_offset"])
        self.prediction_factor = ctk.DoubleVar(value=defaults["prediction_factor"])
        self.humanization = ctk.DoubleVar(value=defaults["humanization"])
        self.lock_stability = ctk.DoubleVar(value=defaults["lock_stability"])
        self.mask_width = ctk.DoubleVar(value=defaults.get("mask_width", 0.0))    
        self.mask_height = ctk.DoubleVar(value=defaults.get("mask_height", 0.0))  
        self.mask_x_offset = ctk.DoubleVar(value=defaults.get("mask_x_offset", 0.0))
        self.mask_y_offset = ctk.DoubleVar(value=defaults.get("mask_y_offset", 0.5))
        self.show_fov = ctk.BooleanVar(value=defaults.get("show_fov", True)) # v0.5.1
        self.mouse_control_var = ctk.BooleanVar(value=defaults["combat_mode"])

    def save_config(self):
        data = {
            "smooth_factor": self.smooth_factor.get(),
            "magnet_smooth": self.magnet_smooth.get(),
            "magnet_radius": self.magnet_radius.get(),
            "conf_threshold": self.conf_threshold.get(),
            "target_offset": self.target_offset.get(),
            "prediction_factor": self.prediction_factor.get(),
            "humanization": self.humanization.get(),
            "lock_stability": self.lock_stability.get(),
            "mask_width": self.mask_width.get(),
            "mask_height": self.mask_height.get(),
            "mask_x_offset": self.mask_x_offset.get(),
            "mask_y_offset": self.mask_y_offset.get(),
            "show_fov": self.show_fov.get(),
            "combat_mode": self.mouse_control_var.get()
        }
        try:
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=4) # Added indent for readability
        except Exception as e:
            print(f"Error saving config: {e}")

    def create_slider(self, label_text, variable, min_val, max_val):
        lbl = ctk.CTkLabel(self.settings_frame, text=f"{label_text}: {variable.get():.2f}", text_color="#aaa", font=("Arial", 10))
        lbl.pack(padx=10, pady=(5, 0))
        
        def update_lbl(val):
            lbl.configure(text=f"{label_text}: {float(val):.2f}")
            if self.use_vision:
                # Update vision engine parameters immediately
                self.vision.conf_threshold = self.conf_threshold.get()
                self.vision.sticky_radius = self.magnet_radius.get()
                self.vision.target_offset = self.target_offset.get()
                self.vision.prediction_factor = self.prediction_factor.get()
                self.vision.lock_stability = self.lock_stability.get()
                self.vision.mask_width = self.mask_width.get()
                self.vision.mask_height = self.mask_height.get()
                self.vision.mask_x_offset = self.mask_x_offset.get()
                self.vision.mask_y_offset = self.mask_y_offset.get()
            self.save_config() # Save config on slider change

        slider = ctk.CTkSlider(self.settings_frame, from_=min_val, to=max_val, variable=variable, command=update_lbl,
                               button_color="#00ff00", progress_color="#00ff00", height=15)
        slider.pack(padx=10, pady=(0, 10))

    def create_group_label(self, text):
        lbl = ctk.CTkLabel(self.settings_frame, text=text, text_color="#00ff00", font=("Orbitron", 10, "bold"))
        lbl.pack(padx=10, pady=(10, 5))

    def toggle_hud(self):
        if self.hud_minimized:
            self.menu_container.pack(fill="x", padx=5)
            self.minimize_btn.configure(text="_")
            self.hud_minimized = False
        else:
            self.menu_container.pack_forget()
            self.minimize_btn.configure(text="□")
            self.hud_minimized = True

    def toggle_settings(self):
        if self.settings_visible:
            self.settings_frame.pack_forget()
            self.settings_visible = False
        else:
            self.settings_frame.pack(after=self.settings_btn, fill="x", padx=10, pady=5)
            self.settings_visible = True

    def vision_loop(self):
        """Runs inference as fast as possible in background."""
        while self.vision_thread_running:
            try:
                # Update params before detection
                # These are already updated by slider command, but good to ensure latest values
                self.vision.conf_threshold = self.conf_threshold.get()
                self.vision.sticky_radius = self.magnet_radius.get()
                self.vision.target_offset = self.target_offset.get()
                self.vision.prediction_factor = self.prediction_factor.get()
                self.vision.lock_stability = self.lock_stability.get()
                self.vision.mask_width = self.mask_width.get()   # v0.5.0
                self.vision.mask_height = self.mask_height.get() # v0.5.0
                
                result = self.vision.detect_screen()
                self.latest_detection = result
            except Exception as e:
                print(f"Vision Loop Error: {e}")

    def open_training_ui(self):
        if self.training_window is None or not self.training_window.winfo_exists():
            self.training_window = TrainingWindow()
            self.training_window.focus()
        else:
            self.training_window.focus()

    def draw_bracket(self, x, y, w, h, length=20, color="#00ff00", thickness=2):
        """Draws clean green corner brackets."""
        self.canvas.create_line(x, y, x + length, y, fill=color, width=thickness)
        self.canvas.create_line(x, y, x, y + length, fill=color, width=thickness)
        self.canvas.create_line(x + w, y, x + w - length, y, fill=color, width=thickness)
        self.canvas.create_line(x + w, y, x + w, y + length, fill=color, width=thickness)
        self.canvas.create_line(x, y + h, x + length, y + h, fill=color, width=thickness)
        self.canvas.create_line(x, y + h, x, y + h - length, fill=color, width=thickness)
        self.canvas.create_line(x + w, y + h, x + w - length, y + h, fill=color, width=thickness)
        self.canvas.create_line(x + w, y + h, x + w, y + h - length, fill=color, width=thickness)

    def draw_hud_elements(self, cx, cy):
        """Draws decorative HUD lines"""
        color = "#00ff00"
        self.canvas.create_line(cx - 30, cy, cx - 10, cy, fill=color, width=1)
        self.canvas.create_line(cx + 10, cy, cx + 30, cy, fill=color, width=1)
        self.canvas.create_line(cx, cy - 30, cx, cy - 10, fill=color, width=1)
        self.canvas.create_line(cx, cy + 10, cx, cy + 30, fill=color, width=1)

    def draw_diagnostics(self):
        """Draws ultra-clean premium diagnostics."""
        import time
        
        # Calculate FPS
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        fps = 1.0 / dt if dt > 0 else 0
        self.fps_list.append(fps)
        if len(self.fps_list) > 20: self.fps_list.pop(0)
        avg_fps = sum(self.fps_list) / len(self.fps_list)

        # Minimalist Top Bar (Top Right)
        panel_x = self.screen_width - 20
        panel_y = 30
        
        status_color = "#00ff00"
        if "ERROR" in self.engine_status: status_color = "#ff0000"
        
        diag_text = f"AXION CORE: {self.engine_status}  |  {avg_fps:.0f} FPS"
        if self.use_vision:
            diag_text += f"  |  {self.vision.last_inference_time*1000:.1f}ms"
            
        # Draw elegant shadow-less text for premium feel
        self.canvas.create_text(panel_x, panel_y, text=diag_text, fill=status_color, anchor="ne", font=("Orbitron", 10))

        # Check for Training Progress (Hidden by default unless active)
        if os.path.exists("training_progress.json"):
            try:
                with open("training_progress.json", "r") as f:
                    p = json.load(f)
                    progress_text = f"NEURAL TRAINING: EPOCH {p.get('epoch', '?')}  |  LOSS: {p.get('loss', 0):.4f}"
                    self.canvas.create_text(panel_x, panel_y + 25, text=progress_text, fill="#00ff00", anchor="ne", font=("Orbitron", 9))
            except:
                pass

    def update_overlay(self):
        """Main loop to update the visualization."""
        self.canvas.delete("all")

        # Static Crosshair
        scx, scy = self.screen_width/2, self.screen_height/2
        self.canvas.create_line(scx-5, scy, scx+5, scy, fill="#00ff00", width=1)
        self.canvas.create_line(scx, scy-5, scx, scy+5, fill="#00ff00", width=1)

        # Draw Diagnostics & FPS
        self.draw_diagnostics()

        # Show Magnet Radius while tuning
        # --- FOV CIRCLE (MAGNET RADIUS) ---
        if self.settings_visible or self.show_fov.get():
            r = self.magnet_radius.get()
            color = "#00ff00" if not self.settings_visible else "#333333"
            self.canvas.create_oval(scx - r, scy - r, scx + r, scy + r, outline=color, dash=(4, 4), width=1)
            
            # --- MASK VISUALIZATION (v0.5.0) ---
            mw = self.mask_width.get()
            mh = self.mask_height.get()
            if mw > 0 or mh > 0:
                # Calculate mask box (Same logic as vision_engine)
                roi_size = self.vision.roi_size if self.use_vision else 640
                m_px_w = roi_size * mw
                m_px_h = roi_size * mh
                
                # Visual center in overlay matches ROI center
                mx_shift = (roi_size // 2) * self.mask_x_offset.get()
                my_shift = (roi_size // 2) * self.mask_y_offset.get()
                
                x1 = scx + mx_shift - m_px_w // 2
                y1 = scy + my_shift - m_px_h // 2
                x2 = scx + mx_shift + m_px_w // 2
                y2 = scy + my_shift + m_px_h // 2
                
                # Draw semi-transparent red box for tuning
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ff0000", stipple="gray25", outline="#ff0000", width=1)
                self.canvas.create_text(x1, y1 - 10, text="MASK ACTIVE", fill="#ff0000", font=("Orbitron", 8), anchor="sw")
            
        x, y, box_w, box_h = 0, 0, 0, 0
        px, py = 0, 0 # Predicted coordinates
        detected = False
        confidence = 0.0

        if self.use_vision:
            target = self.latest_detection
            if target:
                x, y, box_w, box_h, confidence, px, py = target # Unpack predicted coordinates
                detected = True
        else:
            # NO MORE SIMULATION. If vision fails, the user sees nothing but diagnostic error.
            pass

        if detected:
            cx, cy = calculate_centroid(x, y, box_w, box_h)
            # VISUAL REFINE: Apply vertical offset to the HUD circle too
            cy += int(box_h * self.target_offset.get())
            
            self.draw_bracket(x, y, box_w, box_h, length=min(box_w, box_h)//4, color="#00ff00")
            
            # --- MINIMALIST TARGET LABELS ---
            label_x = x + box_w + 8
            self.canvas.create_text(label_x, y, text=f"TARGET // {confidence:.0%}", fill="#00ff00", anchor="nw", font=("Orbitron", 9, "bold"))
            self.canvas.create_text(label_x, y + 15, text=f"{self.vision.last_inference_time*1000:.1f}ms", fill="#00ff00", anchor="nw", font=("Orbitron", 8))
            
            # --- HUD UPDATES ---
            # Current Point (Target)
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="#00ff00", outline="#004400", width=1)
            
            # Prediction Path (Ghost)
            if self.prediction_factor.get() > 0:
                self.canvas.create_line(cx, cy, px, py, fill="#00ff00", dash=(2, 2), width=1)
                self.canvas.create_oval(px - 2, py - 2, px + 2, py + 2, outline="#00ff00", width=1)

            # Combat Logic
            if self.mouse_control_var.get():
                try:
                    from mouse_control import move_mouse_to
                    import math
                    # Aim at predicted point if enabled, else current center
                    aim_x, aim_y = (px, py) if self.prediction_factor.get() > 0 else (cx, cy)
                    dist = math.hypot(aim_x - scx, aim_y - scy)
                    
                    smooth = self.smooth_factor.get()
                    rad = self.magnet_radius.get()
                    
                    if dist < rad: 
                        smooth = self.magnet_smooth.get()
                    
                    move_mouse_to(aim_x, aim_y, smooth_factor=smooth, humanization=self.humanization.get())
                    self.canvas.create_text(scx, 50, text="CORE // MAGNETIC LOCK ACTIVE", fill="#00ff00", font=("Orbitron", 14, "bold"))
                except Exception as e: print(f"Mouse Error: {e}")
        
        self.after(10, self.update_overlay)

    def toggle_combat_mode(self):
        """Toggles the Aim Assist switch."""
        current = self.mouse_control_var.get()
        self.mouse_control_var.set(not current)
        self.save_config() # Save config when combat mode is toggled
        state = "ENABLED" if not current else "DISABLED"
        print(f"Combat Mode {state}")

if __name__ == "__main__":
    app = OverlayApp()
    app.mainloop()
