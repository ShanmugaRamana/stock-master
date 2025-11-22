import tkinter as tk
from tkinter import messagebox

# Import Views
from windows.navigation.overview import OverviewView
from windows.navigation.products import ProductsView
from windows.navigation.stock import StockView
from windows.navigation.operations import OperationsView
from windows.navigation.history import HistoryView
from windows.navigation.profile import ProfileView # <--- NEW IMPORT

class DashboardScreen:
    def __init__(self, root, user_details=None):
        self.root = root
        self.user_details = user_details or {}
        self.root.title("Dashboard - Stock Master")
        
        # Colors
        self.color_header = "#1f2937"       
        self.color_header_hover = "#374151" 
        self.color_header_active = "#4b5563" 
        self.color_bg = "#f3f4f6"           
        self.color_text_nav = "#e5e7eb"     
        
        self.nav_buttons = {} 

        self.setup_window()
        self.setup_ui()

        # Load Overview by default
        self.load_view("Overview", OverviewView)

    def setup_window(self):
        try:
            self.root.state('zoomed')
        except tk.TclError:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{w}x{h}+0+0")
        
        self.root.configure(bg=self.color_bg)

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- 1. HEADER SECTION ---
        header_frame = tk.Frame(self.root, bg=self.color_header, height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False) 

        # Branding
        brand_frame = tk.Frame(header_frame, bg=self.color_header)
        brand_frame.pack(side="left", padx=20)
        tk.Label(brand_frame, text="*", font=("Courier", 30), fg="white", bg=self.color_header).pack(side="left")
        tk.Label(brand_frame, text="STOCK MASTER", font=("Helvetica", 14, "bold"), fg="white", bg=self.color_header).pack(side="left", padx=10)

        # Navigation Links
        nav_frame = tk.Frame(header_frame, bg=self.color_header)
        nav_frame.pack(side="left", padx=40)

        self.create_nav_btn(nav_frame, "Overview", lambda: self.load_view("Overview", OverviewView))
        self.create_nav_btn(nav_frame, "Products", lambda: self.load_view("Products", ProductsView))
        self.create_nav_btn(nav_frame, "Stock", lambda: self.load_view("Stock", StockView))
        self.create_nav_btn(nav_frame, "Operations", lambda: self.load_view("Operations", OperationsView))
        self.create_nav_btn(nav_frame, "Move History", lambda: self.load_view("Move History", HistoryView))

        # Profile Menu
        profile_frame = tk.Frame(header_frame, bg=self.color_header)
        profile_frame.pack(side="right", padx=20)

        display_name = self.user_details.get("email", self.user_details.get("username", "User"))
        
        self.mb_profile = tk.Menubutton(profile_frame, text=f"  {display_name} ▼", font=("Helvetica", 11), 
                                        fg="white", bg=self.color_header, 
                                        activebackground=self.color_header_hover, activeforeground="white",
                                        relief="flat", cursor="hand2", bd=0)
        
        self.menu_profile = tk.Menu(self.mb_profile, tearoff=0, bg="white", fg="#333", font=("Helvetica", 10))
        self.menu_profile.add_command(label="My Profile", command=self.action_profile) # <--- Triggers profile view
        self.menu_profile.add_separator()
        self.menu_profile.add_command(label="Logout", command=self.action_logout)
        
        self.mb_profile.config(menu=self.menu_profile)
        self.mb_profile.pack(side="right", ipady=10)

        # --- 2. MAIN CONTENT AREA ---
        self.content_frame = tk.Frame(self.root, bg=self.color_bg)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)

    def create_nav_btn(self, parent, name, command):
        btn = tk.Button(parent, text=name, font=("Helvetica", 11), 
                        bg=self.color_header, fg=self.color_text_nav,
                        activebackground=self.color_header_active, activeforeground="white",
                        relief="flat", bd=0, cursor="hand2", 
                        command=command)
        btn.pack(side="left", padx=2, ipady=10, ipadx=15)
        
        self.nav_buttons[name] = btn

        btn.bind("<Enter>", lambda e: self.on_hover(name))
        btn.bind("<Leave>", lambda e: self.on_leave(name))

    def load_view(self, view_name, view_class):
        self.current_view = view_name
        
        # Highlight active button (if it exists in nav bar)
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.config(bg=self.color_header_active, fg="white")
            else:
                btn.config(bg=self.color_header, fg=self.color_text_nav)

        # Clear Content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Initialize View
        # Smart init: Try passing 'self' (dashboard) as second arg; if it fails, use standard init
        try:
            view_class(self.content_frame, self)
        except TypeError:
            view_class(self.content_frame)

    def on_hover(self, name):
        if self.current_view != name:
            self.nav_buttons[name].config(bg=self.color_header_hover, fg="white")

    def on_leave(self, name):
        if self.current_view != name:
            self.nav_buttons[name].config(bg=self.color_header, fg=self.color_text_nav)

    def action_profile(self):
        # Switch main view to Profile
        self.load_view("Profile", ProfileView)

    def action_logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            from windows.login import LoginScreen
            LoginScreen(self.root)