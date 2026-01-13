import customtkinter as ctk
from overlay import OverlayApp

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = OverlayApp()
    app.mainloop()

if __name__ == "__main__":
    main()
