import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
from ultralytics import YOLO
import os

class TrainingWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
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
        
        # Dataset Selection
        self.select_ds_btn = ctk.CTkButton(self.left_panel, text="Select Image Folder", 
                                           command=self.select_dataset_folder, fg_color="#333", border_color="#666", border_width=1)
        self.select_ds_btn.pack(pady=10, padx=20, fill="x")
        
        self.selected_path_label = ctk.CTkLabel(self.left_panel, text="No folder selected", text_color="#666", wraplength=200)
        self.selected_path_label.pack(pady=(0, 20))
        
        self.yaml_path = None
        
        # Params
        self.epochs_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Epochs (e.g. 50)")
        self.epochs_entry.insert(0, "10")
        self.epochs_entry.pack(pady=5, padx=20, fill="x")
        
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
            
            # Check for data.yaml, if not exist, create it
            yaml_path = os.path.join(folder_path, "data.yaml")
            if not os.path.exists(yaml_path):
                self.log("No data.yaml found. Generating auto-config...")
                try:
                    with open(yaml_path, 'w') as f:
                        # Simple config assuming images are in the folder
                        # Note: YOLO usually expects 'train/images' structure, but absolute paths work too.
                        # We set 'train' and 'val' to the selected folder.
                        f.write(f"path: {folder_path}\n")
                        f.write(f"train: .\n")
                        f.write(f"val: .\n")
                        f.write("names:\n  0: Target\n")
                    self.log(f"Created config: {yaml_path}")
                except Exception as e:
                    self.log(f"Error creating yaml: {e}")
                    return
            else:
                self.log("Found existing data.yaml.")
                
            self.yaml_path = yaml_path

    def log(self, message):
        self.console_out.insert("end", message + "\n")
        self.console_out.see("end")

    def start_training_thread(self):
        if not self.yaml_path:
            self.log("ERROR: Please select a data.yaml file first.")
            return
            
        if self.training_active:
            self.log("WARNING: Training already in progress.")
            return

        self.training_active = True
        self.train_btn.configure(text="TRAINING RUNNING...", state="disabled", fg_color="#550000")
        
        epochs = 10
        try:
            epochs = int(self.epochs_entry.get())
        except:
            pass
            
        # Start in thread to not freeze UI
        t = threading.Thread(target=self.run_yolo_train, args=(self.yaml_path, epochs))
        t.start()

    def run_yolo_train(self, data_path, epochs):
        self.log(f"Initializing YOLOv8n training for {epochs} epochs...")
        self.log("Downloading model if needed...")
        
        try:
            model = YOLO('yolov8n.pt')
            
            # Train
            self.log("Starting training process...")
            results = model.train(data=data_path, epochs=epochs, imgsz=640)
            
            self.log("Training Complete!")
            self.log(f"Results saved to: {results.save_dir}")
            
        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}")
        
        self.training_active = False
        self.train_btn.configure(text="START REAL TRAINING", state="normal", fg_color="#004400")
