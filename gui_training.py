import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from ultralytics import YOLO
import os
import sys

# Validate CustomTkinter is effectively imported
try:
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
except Exception as e:
    print(f"Error init CTK: {e}")

class TrainingWindow(ctk.CTk): # Changed from Toplevel to CTk for standalone running
    def __init__(self):
        super().__init__()
        self.title("Training & Dataset Management")
        self.geometry("800x600")
        self.configure(fg_color="#0d0d0d")
        self.training_active = False
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", height=60, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        
        self.label = ctk.CTkLabel(self.header_frame, text="YOLO TRAINING CONTROL", 
                                  font=("Orbitron", 20, "bold"), text_color="#00ff00")
        self.label.pack(pady=15)
        
        # Content Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left: Config
        self.left_panel = ctk.CTkFrame(self.grid_frame, fg_color="#1a1a1a", corner_radius=10, border_width=1, border_color="#333")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.ds_label = ctk.CTkLabel(self.left_panel, text="Configuration", font=("Arial", 14, "bold"), text_color="white")
        self.ds_label.pack(pady=(15, 10))

        # Initial Environment Check
        self.check_environment()
        
    def check_environment(self):
        """Auto-detects GPU and libraries."""
        try:
            import torch
            import ultralytics
            try:
                 # Attempt to load a small model to verify
                pass
            except:
                pass
                
            self.is_gpu = False
            device = "CPU"
            
            if torch.cuda.is_available():
                device = f"NVIDIA GPU ({torch.cuda.get_device_name(0)})"
                self.is_gpu = True
            elif torch.backends.mps.is_available():
                device = "APPLE SILICON (MPS)"
                
            print(f"✅ Environment OK. Device: {device}")
            if not self.is_gpu and not torch.backends.mps.is_available():
                print("⚠️ WARNING: RUNNING ON CPU. TRAINING WILL BE SLOW.")
                print("👉 Use 'install_gpu.bat' to enable your RTX card.")
            # We can't update UI here easily as it's init, but print is good.
        except ImportError as e:
            print(f"❌ CRITICAL MISSING LIB: {e}")
        
        # Dataset Selection
        self.select_ds_btn = ctk.CTkButton(self.left_panel, text="Select Image Folder", 
                                           command=self.select_dataset_folder, fg_color="#333", border_color="#666", border_width=1)
        self.select_ds_btn.pack(pady=10, padx=20, fill="x")
        
        self.selected_path_label = ctk.CTkLabel(self.left_panel, text="No folder selected", text_color="#666", wraplength=200)
        self.selected_path_label.pack(pady=(0, 20))
        
        self.yaml_path = None
        self.base_model_path = 'yolov8n.pt' # Default to new training
        
        # Base Model Selection
        self.model_btn = ctk.CTkButton(self.left_panel, text="Select Base Model (Optional)", 
                                       command=self.select_base_model, fg_color="#444", border_color="#666", border_width=1)
        self.model_btn.pack(pady=10, padx=20, fill="x")
        self.model_label = ctk.CTkLabel(self.left_panel, text="Base: yolov8n.pt (Fresh)", text_color="gray", font=("Arial", 10))
        self.model_label.pack(pady=(0, 10))
        
        # Params
        self.epochs_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Epochs")
        # Smart Default: 100 for GPU, 50 for others
        default_epochs = "100" if getattr(self, "is_gpu", False) else "50"
        self.epochs_entry.insert(0, default_epochs)
        self.epochs_entry.pack(pady=5, padx=20, fill="x")
        
        reco_text = "Recommended: 100+ (RTX Detected)" if getattr(self, "is_gpu", False) else "Recommended: 50 (CPU/MPS)"
        ctk.CTkLabel(self.left_panel, text=reco_text, text_color="gray", font=("Arial", 10)).pack(pady=(0, 10))
        
        # Device Force
        self.device_var = ctk.StringVar(value="Auto")
        self.device_menu = ctk.CTkOptionMenu(self.left_panel, values=["Auto", "GPU (0)", "CPU"], variable=self.device_var)
        self.device_menu.pack(pady=10, padx=20, fill="x")
        
        # Right: Output
        self.right_panel = ctk.CTkFrame(self.grid_frame, fg_color="#1a1a1a", corner_radius=10, border_width=1, border_color="#333")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.status_label = ctk.CTkLabel(self.right_panel, text="Training Output", font=("Arial", 14, "bold"), text_color="white")
        self.status_label.pack(pady=(15, 10))
        
        self.console_out = ctk.CTkTextbox(self.right_panel, fg_color="#000", text_color="#0f0", font=("Courier", 10))
        self.console_out.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.train_btn = ctk.CTkButton(self.right_panel, text="START REAL TRAINING", 
                                       font=("Arial", 12, "bold"),
                                       fg_color="#004400", hover_color="#006600", 
                                       border_color="#00ff00", border_width=2,
                                       command=self.start_training_thread)
        self.train_btn.pack(pady=20)

    def select_dataset_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_path_label.configure(text=os.path.basename(folder_path), text_color="#ccc")
            self.log(f"Selected folder: {folder_path}")
            
            # Validate Dataset
            valid, msg = self.validate_dataset(folder_path)
            if not valid:
                self.log(f"⚠️ DATASET WARNING: {msg}")
            
            # Create/Update config
            yaml_path = os.path.join(folder_path, "data.yaml")
            self.log("Generating smart config...")
            try:
                with open(yaml_path, 'w') as f:
                    # Use absolute path ensures YOLO finds it regardless of where it's run
                    abs_path = os.path.abspath(folder_path)
                    f.write(f"path: {abs_path}\n")
                    f.write(f"train: .\n") 
                    f.write(f"val: .\n") 
                    # Assuming standard classes, but ideally this is customizable
                    f.write("names:\n  0: Target\n")
                self.log(f"✅ Config created: {yaml_path}")
                self.yaml_path = yaml_path
            except Exception as e:
                self.log(f"❌ Error creating yaml: {e}")
                self.yaml_path = None

    def select_base_model(self):
        path = filedialog.askopenfilename(filetypes=[("YOLO Model", "*.pt")])
        if path:
            self.base_model_path = path
            self.model_label.configure(text=f"Base: {os.path.basename(path)} (Fine-Tuning)")
            self.log(f"🧠 Base Model set to: {os.path.basename(path)}")
            self.log("   -> New dataset will refine this model (Transfer Learning).")

    def validate_dataset(self, path):
        """Checks if the folder actually contains images and labels."""
        images = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        labels = [f for f in os.listdir(path) if f.lower().endswith('.txt') and f != "classes.txt"]
        
        if not images:
            return False, "No images found in folder!"
        if len(images) > 0 and len(labels) == 0:
            return False, "Found images but NO label files (.txt). Model will learn nothing!"
        
        # Simple ratio check
        if len(labels) < len(images) * 0.5:
             return True, f"Warning: Only {len(labels)} labels for {len(images)} images. Some data is unlabeled."
             
        self.log(f"📊 Dataset Stats: {len(images)} Images, {len(labels)} Labels.")
        return True, "Dataset looks healthy."

    def log(self, message):
        self.console_out.insert("end", message + "\n")
        self.console_out.see("end")

    def start_training_thread(self):
        if not self.yaml_path:
            self.log("❌ ERROR: Please select a valid dataset first.")
            return
            
        if self.training_active:
            self.log("⚠️ Training already in progress.")
            return

        self.training_active = True
        self.train_btn.configure(text="TRAINING IN PROGRESS...", state="disabled", fg_color="#550000")
        
        epochs = 10
        try:
            epochs = int(self.epochs_entry.get())
        except:
            pass
            
        # Start in thread
        # Start in thread
        selected_device = self.device_var.get()
        t = threading.Thread(target=self.run_yolo_train, args=(self.yaml_path, epochs, self.base_model_path, selected_device))
        t.start()

    def run_yolo_train(self, data_path, epochs, base_model, device_mode):
        self.log(f"🚀 Initializing Training ({epochs} epochs)...")
        self.log(f"🧠 Base Model: {os.path.basename(base_model)}")
        self.log("Note: Results will be saved to the 'runs' folder.")
        
        try:
            # Check for GPU
            import torch
            device = 'cpu'
            
            if device_mode == "GPU (0)":
                 device = '0'
            elif device_mode == "CPU":
                 device = 'cpu'
            else: # Auto
                if torch.cuda.is_available(): device = '0'
                elif torch.backends.mps.is_available(): device = 'mps'
            
            self.log(f"💻 Compute Device: {str(device).upper()}")
            
            model = YOLO(base_model) # Load selected model
            
            self.log("Starting training process... (Check terminal for detailed progress)")
            
            # Run training
            results = model.train(
                data=data_path, 
                epochs=epochs, 
                imgsz=640, 
                device=device,
                plots=True,
                batch=-1, # Auto-batch to maximize memory usage specifically for 4000 images
                save=True
            )
            
            self.log("✅ Training Complete!")
            self.log(f"💾 Model saved to: {results.save_dir}")
            
        except Exception as e:
            self.log(f"❌ CRITICAL ERROR: {str(e)}")
            self.log("Tip: If Out Of Memory (OOM), close other apps or reduce batch size.")
        
        self.training_active = False
        self.train_btn.configure(text="START REAL TRAINING", state="normal", fg_color="#004400")

if __name__ == "__main__":
    app = TrainingWindow()
    app.mainloop()
