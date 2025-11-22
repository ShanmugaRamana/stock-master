import tkinter as tk
from tkinter import ttk, messagebox
import requests

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Stock Master")
        self.API_URL = "http://127.0.0.1:8000"
        
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
        for widget in self.root.winfo_children():
            widget.destroy()

        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True)
        main_container.grid_columnconfigure(0, weight=1, uniform="half_split")
        main_container.grid_columnconfigure(1, weight=1, uniform="half_split")
        main_container.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDE ---
        self.canvas_left = tk.Canvas(main_container, highlightthickness=0)
        self.canvas_left.grid(row=0, column=0, sticky="nsew")
        self.draw_gradient(self.canvas_left, "#ff9966", "#ff5e62")
        
        screen_h = self.root.winfo_screenheight()
        self.canvas_left.create_text(50, 60, text="*", font=("Courier", 70), fill="white", anchor="nw")
        self.canvas_left.create_text(50, screen_h - 270, text="Seamless Management", font=("Helvetica", 14), fill="#FFF1F2", anchor="w")
        self.canvas_left.create_text(50, screen_h - 180, text="Empower your business\nwith intelligent stock\ncontrol.", font=("Helvetica", 28, "bold"), fill="white", anchor="w", justify="left")

        # --- RIGHT SIDE ---
        frame_right = tk.Frame(main_container, bg=self.color_bg_right)
        frame_right.grid(row=0, column=1, sticky="nsew")
        
        login_card = tk.Frame(frame_right, bg=self.color_bg_right)
        login_card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_card, text="*", font=("Courier", 50), fg=self.color_primary, bg=self.color_bg_right).pack(anchor="w")
        tk.Label(login_card, text="Welcome Back", font=("Helvetica", 26, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w")
        tk.Label(login_card, text="Sign in to manage inventory, sales, and reports.", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(anchor="w", pady=(5, 30))

        tk.Label(login_card, text="Username / ID", font=("Helvetica", 10, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w", pady=(0, 5))
        self.entry_user = tk.Entry(login_card, font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_user.pack(ipady=8, pady=(0, 20))

        tk.Label(login_card, text="Password", font=("Helvetica", 10, "bold"), fg=self.color_text_head, bg=self.color_bg_right).pack(anchor="w", pady=(0, 5))
        self.entry_pass = tk.Entry(login_card, show="*", font=("Helvetica", 11), width=40, bg=self.color_input_bg, relief="flat", highlightthickness=1, highlightbackground=self.color_border, highlightcolor="#333")
        self.entry_pass.pack(ipady=8, pady=(0, 5))

        btn_forgot = tk.Button(login_card, text="Forgot Password?", font=("Helvetica", 9), fg=self.color_text_sub, bg=self.color_bg_right, activebackground=self.color_bg_right, activeforeground=self.color_primary, cursor="hand2", relief="flat", borderwidth=0, command=self.open_forgot)
        btn_forgot.pack(anchor="e", pady=(0, 20))

        # --- UPDATED LOGIN BUTTON ---
        btn_login = tk.Button(login_card, text="Login to Dashboard", font=("Helvetica", 11, "bold"), bg=self.color_primary, fg="white", activebackground="#333333", activeforeground="white", cursor="hand2", relief="flat", borderwidth=0, 
                              command=self.handle_login) # Linked to logic
        btn_login.pack(fill="x", ipady=10)
        
        footer_frame = tk.Frame(login_card, bg=self.color_bg_right)
        footer_frame.pack(pady=20)
        
        tk.Label(footer_frame, text="Don't have an account?", font=("Helvetica", 10), fg=self.color_text_sub, bg=self.color_bg_right).pack(side="left")
        btn_signup = tk.Button(footer_frame, text="Sign up", font=("Helvetica", 10, "bold"), fg=self.color_primary, bg=self.color_bg_right, cursor="hand2", relief="flat", borderwidth=0, activebackground="white", command=self.open_signup)
        btn_signup.pack(side="left", padx=5)
        
        self.canvas_left.bind("<Configure>", lambda e: self.draw_gradient(self.canvas_left, "#ff9966", "#ff5e62"))

    def handle_login(self):
        login_id = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not login_id or not password:
            messagebox.showwarning("Input Error", "Please enter both Login ID and Password.")
            return

        payload = {"login_id": login_id, "password": password}

        try:
            response = requests.post(f"{self.API_URL}/login", json=payload)
            
            if response.status_code == 200:
                user_data = response.json()
                # Open Dashboard
                self.open_dashboard(user_data)
            else:
                # Parse Error
                try:
                    error_msg = response.json().get("detail", "Login Failed")
                except:
                    error_msg = "Login Failed"
                messagebox.showerror("Error", error_msg)

        except requests.exceptions.ConnectionError:
             messagebox.showerror("Connection Error", "Cannot connect to server.")

    def open_dashboard(self, user_data):
        from windows.dashboard import DashboardScreen
        DashboardScreen(self.root, user_details=user_data)

    def open_signup(self):
        from windows.signup import SignupScreen
        SignupScreen(self.root)

    def open_forgot(self):
        from windows.forgot_password import ForgotPasswordScreen
        ForgotPasswordScreen(self.root)

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