import tkinter as tk
from tkinter import ttk

class ForgotPasswordScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Forgot Password - Stock Master")
        
        # Colors
        self.color_bg_right = "white"
        self.color_primary = "#000000" 
        self.color_text_head = "#111827"
        self.color_text_sub = "#6B7280"
        self.color_input_bg = "#F9FAFB"
        self.color_border = "#E5E7EB"
        
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        try:
            self.root.state('zoomed')
        except tk.TclError:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}+0+0")
        self.root.resizable(False, False)

    def setup_ui(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        main_container.grid_columnconfigure(0, weight=1, uniform="half_split")
        main_container.grid_columnconfigure(1, weight=1, uniform="half_split")
        main_container.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDE (Gradient) ---
        self.canvas_left = tk.Canvas(main_container, highlightthickness=0)
        self.canvas_left.grid(row=0, column=0, sticky="nsew")
        self.draw_gradient(self.canvas_left, "#ff9966", "#ff5e62")
        
        screen_h = self.root.winfo_screenheight()
        self.canvas_left.create_text(50, 60, text="*", font=("Courier", 70), fill="white", anchor="nw")
        self.canvas_left.create_text(50, screen_h - 270, text="Security First", font=("Helvetica", 14), fill="#FFF1F2", anchor="w")
        self.canvas_left.create_text(50, screen_h - 180, text="Recover access to\nyour dashboard\nsecurely.", font=("Helvetica", 28, "bold"), fill="white", anchor="w", justify="left")

        # --- RIGHT SIDE (Form) ---
        frame_right = tk.Frame(main_container, bg=self.color_bg_right)
        frame_right.grid(row=0, column=1, sticky="nsew")
        
        card = tk.Frame(frame_right, bg=self.color_bg_right)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="*", font=("Courier", 50), fg=self.color_primary, bg=self.color_bg_right).pack(anchor="w")
        tk.Label(card, text="Reset Password", font=("Helvetica", 26, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        tk.Label(card, text="Enter your email to receive reset instructions.", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(anchor="w", pady=(5, 30))

        # Input
        tk.Label(card, text="Email Address", font=("Helvetica", 10, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w", pady=(0, 5))
        self.entry_email = tk.Entry(card, font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_email.pack(ipady=8, pady=(0, 30))

        # Submit Button
        btn_send = tk.Button(card, text="Send Reset Link", font=("Helvetica", 11, "bold"), bg=self.color_primary, fg="white", activebackground="#333333", activeforeground="white", cursor="hand2", relief="flat", borderwidth=0)
        btn_send.pack(fill="x", ipady=10)
        
        # Footer
        footer_frame = tk.Frame(card, bg=self.color_bg_right)
        footer_frame.pack(pady=20)
        
        tk.Label(footer_frame, text="Remembered your password?", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(side="left")
        
        # Back to Login
        btn_back = tk.Button(footer_frame, text="Login", font=("Helvetica", 10, "bold"), fg=self.color_primary, bg=self.color_bg_right, cursor="hand2", relief="flat", borderwidth=0, activebackground="white", command=self.open_login)
        btn_back.pack(side="left", padx=5)
        
        self.canvas_left.bind("<Configure>", lambda e: self.draw_gradient(self.canvas_left, "#ff9966", "#ff5e62"))

    def open_login(self):
        from windows.login import LoginScreen
        LoginScreen(self.root)

    def draw_gradient(self, canvas, color1, color2):
        width = self.root.winfo_screenwidth() // 2 
        height = self.root.winfo_screenheight()
        canvas.delete("gradient")
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        steps = 100
        for i in range(steps):
            r, g, b = int(r1 + (r2 - r1) * i / steps), int(g1 + (g2 - g1) * i / steps), int(b1 + (b2 - b1) * i / steps)
            color = f'#{r:02x}{g:02x}{b:02x}'
            y0, y1 = i * (height / steps), (i + 1) * (height / steps)
            canvas.create_rectangle(0, y0, width + 200, y1 + 2, fill=color, outline=color, tags="gradient")
        canvas.tag_lower("gradient")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))