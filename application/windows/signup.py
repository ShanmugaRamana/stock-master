import tkinter as tk
from tkinter import ttk

class SignupScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up - Stock Master")
        
        # Colors (Same as Login)
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
        # Clear any existing content (from Login page)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
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
        self.canvas_left.create_text(50, screen_h - 270, text="Join the Ecosystem", font=("Helvetica", 14), fill="#FFF1F2", anchor="w")
        self.canvas_left.create_text(50, screen_h - 180, text="Start your journey\ntowards organized\ngrowth.", font=("Helvetica", 28, "bold"), fill="white", anchor="w", justify="left")

        # --- RIGHT SIDE (Sign Up Form) ---
        frame_right = tk.Frame(main_container, bg=self.color_bg_right)
        frame_right.grid(row=0, column=1, sticky="nsew")
        
        signup_card = tk.Frame(frame_right, bg=self.color_bg_right)
        signup_card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(signup_card, text="*", font=("Courier", 40), fg=self.color_primary, bg=self.color_bg_right).pack(anchor="w", pady=(0, 0))
        tk.Label(signup_card, text="Create Account", font=("Helvetica", 24, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        tk.Label(signup_card, text="Enter your details to get started.", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(anchor="w", pady=(5, 20))

        # -- 1. Login ID --
        tk.Label(signup_card, text="Login ID", font=("Helvetica", 9, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        self.entry_user = tk.Entry(signup_card, font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_user.pack(ipady=6, pady=(0, 10))

        # -- 2. Email ID --
        tk.Label(signup_card, text="Email ID", font=("Helvetica", 9, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        self.entry_email = tk.Entry(signup_card, font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_email.pack(ipady=6, pady=(0, 10))

        # -- 3. Password --
        tk.Label(signup_card, text="Password", font=("Helvetica", 9, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        self.entry_pass = tk.Entry(signup_card, show="*", font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_pass.pack(ipady=6, pady=(0, 10))

        # -- 4. Re-enter Password --
        tk.Label(signup_card, text="Re-enter Password", font=("Helvetica", 9, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        self.entry_repass = tk.Entry(signup_card, show="*", font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_repass.pack(ipady=6, pady=(0, 20))

        # -- Button --
        btn_create = tk.Button(signup_card, text="Create Account", font=("Helvetica", 11, "bold"), bg=self.color_primary, fg="white", activebackground="#333333", activeforeground="white", cursor="hand2", relief="flat", borderwidth=0)
        btn_create.pack(fill="x", ipady=10)
        
        # -- Footer --
        footer_frame = tk.Frame(signup_card, bg=self.color_bg_right)
        footer_frame.pack(pady=20)
        tk.Label(footer_frame, text="Already have an account?", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(side="left")
        
        # COMMAND TO GO BACK TO LOGIN
        btn_login = tk.Button(footer_frame, text="Login", font=("Helvetica", 10, "bold"), fg=self.color_primary, bg=self.color_bg_right, cursor="hand2", relief="flat", borderwidth=0, activebackground="white", command=self.open_login)
        btn_login.pack(side="left", padx=5)
        
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