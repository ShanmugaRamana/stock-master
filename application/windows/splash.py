import tkinter as tk
from tkinter import ttk

class SplashScreen:
    def __init__(self, root, on_complete_callback):
        self.root = root
        self.on_complete = on_complete_callback
        
        # Create Toplevel window for Splash
        self.window = tk.Toplevel(root)
        self.window.title("Loading...")
        self.window.overrideredirect(True) # No borders
        
        # Dimensions
        width = 500
        height = 300
        self.center_window(width, height)
        
        # UI Content
        self.setup_ui(width, height)
        
        # Start Loading
        self.update_progress(0)

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self, width, height):
        # Use Canvas for Gradient Background
        self.canvas = tk.Canvas(self.window, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Draw Gradient (Sunset Matte)
        self.draw_gradient(self.canvas, "#ff9966", "#ff5e62", width, height)
        
        # Add Star Logo
        self.canvas.create_text(width//2, 100, text="*", font=("Courier", 100), fill="white", anchor="center")
        
        # Add App Name
        self.canvas.create_text(width//2, 180, text="STOCK MASTER", font=("Helvetica", 20, "bold"), fill="white", anchor="center")
        
        # Add Loading Text
        self.label_loading = self.canvas.create_text(width//2, 230, text="Initializing Application...", font=("Helvetica", 10), fill="#FFF1F2", anchor="center")
        
        # Custom Style for Progress Bar to look decent on gradient
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Splash.Horizontal.TProgressbar", background="white", troughcolor="#cc4444", bordercolor="#ff5e62")
        
        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=400, mode="determinate", style="Splash.Horizontal.TProgressbar")
        # Place progress bar on top of canvas
        self.progress.place(relx=0.5, rely=0.85, anchor="center")

    def draw_gradient(self, canvas, color1, color2, width, height):
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        steps = height
        
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def update_progress(self, value):
        self.progress['value'] = value
        if value < 100:
            # Update every 30ms
            self.window.after(30, lambda: self.update_progress(value + 2))
        else:
            # Loading Complete
            self.window.destroy()
            self.on_complete()