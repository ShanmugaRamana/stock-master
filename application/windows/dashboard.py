import tkinter as tk
from tkinter import messagebox

class DashboardScreen:
    def __init__(self, root, user_details=None):
        self.root = root
        self.user_details = user_details or {}
        self.root.title("Dashboard - Stock Master")
        
        # Colors
        self.color_header = "#1f2937"       # Dark Gray
        self.color_header_hover = "#374151" # Lighter Gray for hover
        self.color_bg = "#f3f4f6"           # Light Gray Background
        self.color_text_nav = "#e5e7eb"     # Off-white
        
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        try:
            self.root.state('zoomed')
        except tk.TclError:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}+0+0")
        
        self.root.configure(bg=self.color_bg)

    def setup_ui(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- 1. HEADER SECTION ---
        header_frame = tk.Frame(self.root, bg=self.color_header, height=60)
        header_frame.pack(fill="x", side="top")
        # Prevent frame from shrinking to fit content (keeps height consistent)
        header_frame.pack_propagate(False) 

        # A. Branding (Left)
        brand_frame = tk.Frame(header_frame, bg=self.color_header)
        brand_frame.pack(side="left", padx=20)
        
        tk.Label(brand_frame, text="*", font=("Courier", 30), fg="white", bg=self.color_header).pack(side="left")
        tk.Label(brand_frame, text="STOCK MASTER", font=("Helvetica", 14, "bold"), fg="white", bg=self.color_header).pack(side="left", padx=10)

        # B. Navigation Links (Center-ish / Left aligned after logo)
        nav_frame = tk.Frame(header_frame, bg=self.color_header)
        nav_frame.pack(side="left", padx=40)

        # Create Nav Buttons
        self.create_nav_btn(nav_frame, "Products", self.nav_products)
        self.create_nav_btn(nav_frame, "Stock", self.nav_stock)
        self.create_nav_btn(nav_frame, "Move History", self.nav_history)
        self.create_nav_btn(nav_frame, "Settings", self.nav_settings)

        # C. Profile Menu (Right)
        profile_frame = tk.Frame(header_frame, bg=self.color_header)
        profile_frame.pack(side="right", padx=20)

        username = self.user_details.get("username", "User")
        
        # Menubutton for Dropdown
        self.mb_profile = tk.Menubutton(profile_frame, text=f"  {username} ▼", font=("Helvetica", 11), 
                                        fg="white", bg=self.color_header, 
                                        activebackground=self.color_header_hover, activeforeground="white",
                                        relief="flat", cursor="hand2", bd=0)
        
        # The actual menu
        self.menu_profile = tk.Menu(self.mb_profile, tearoff=0, bg="white", fg="#333", font=("Helvetica", 10))
        self.menu_profile.add_command(label="My Profile", command=self.action_profile)
        self.menu_profile.add_separator()
        self.menu_profile.add_command(label="Logout", command=self.action_logout)
        
        self.mb_profile.config(menu=self.menu_profile)
        self.mb_profile.pack(side="right", ipady=10)


        # --- 2. MAIN CONTENT AREA ---
        self.content_frame = tk.Frame(self.root, bg=self.color_bg)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Default Content
        tk.Label(self.content_frame, text="Dashboard Overview", font=("Helvetica", 24, "bold"), bg=self.color_bg, fg="#111827").pack(anchor="w")
        tk.Label(self.content_frame, text="Select an option from the menu to get started.", font=("Helvetica", 12), bg=self.color_bg, fg="#6b7280").pack(anchor="w", pady=5)


    # --- HELPER FUNCTIONS ---
    def create_nav_btn(self, parent, text, command):
        """Creates a standardized navigation button with hover effects"""
        btn = tk.Button(parent, text=text, font=("Helvetica", 11), 
                        bg=self.color_header, fg=self.color_text_nav,
                        activebackground=self.color_header_hover, activeforeground="white",
                        relief="flat", bd=0, cursor="hand2", 
                        command=command)
        btn.pack(side="left", padx=2, ipady=10, ipadx=15)
        
        # Hover Effects
        btn.bind("<Enter>", lambda e: btn.config(bg=self.color_header_hover, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.color_header, fg=self.color_text_nav))

    # --- NAVIGATION ACTIONS (Placeholders) ---
    def nav_products(self):
        print("Navigating to Products...")
        # We will implement page switching logic later
    
    def nav_stock(self):
        print("Navigating to Stock...")

    def nav_history(self):
        print("Navigating to Move History...")

    def nav_settings(self):
        print("Navigating to Settings...")

    # --- PROFILE ACTIONS ---
    def action_profile(self):
        messagebox.showinfo("Profile", f"User: {self.user_details.get('username')}\nID: {self.user_details.get('user_id')}")

    def action_logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            from windows.login import LoginScreen
            LoginScreen(self.root)