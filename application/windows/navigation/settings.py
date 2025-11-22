import tkinter as tk
from tkinter import ttk, messagebox

class SettingsView:
    def __init__(self, parent):
        self.parent = parent
        # Main container
        self.frame = tk.Frame(parent, bg="#f3f4f6")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.setup_header()
        self.setup_content()

    def setup_header(self):
        header_frame = tk.Frame(self.frame, bg="#f3f4f6")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="Settings", font=("Helvetica", 24, "bold"), fg="#111827", bg="#f3f4f6").pack(side="left")

    def setup_content(self):
        # We create specific sections (Cards)
        
        # --- SECTION 1: ACCOUNT SETTINGS ---
        self.create_section("Account Settings", self.account_content)

        # --- SECTION 2: PREFERENCES ---
        self.create_section("Application Preferences", self.prefs_content)

        # --- SECTION 3: SYSTEM INFO ---
        self.create_section("System Information", self.about_content)

    def create_section(self, title, content_filler_func):
        """Helper to create consistent white cards for sections"""
        card = tk.Frame(self.frame, bg="white", padx=30, pady=20, relief="flat")
        card.pack(fill="x", pady=(0, 15))
        
        # Section Title
        tk.Label(card, text=title, font=("Helvetica", 14, "bold"), fg="#111827", bg="white").pack(anchor="w", pady=(0, 10))
        
        # Visual Separator
        ttk.Separator(card, orient='horizontal').pack(fill='x', pady=(0, 20))
        
        # Content Container
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="x")
        
        # Call the specific function to fill this frame
        content_filler_func(content_frame)

    def account_content(self, parent):
        """Content for Account Card"""
        # Grid Layout for aligned Label: Value pairs
        tk.Label(parent, text="Login ID:", font=("Helvetica", 10, "bold"), bg="white", fg="#6b7280").grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(parent, text="admin_user", font=("Helvetica", 10), bg="white", fg="#111827").grid(row=0, column=1, sticky="w", padx=30)

        tk.Label(parent, text="Email:", font=("Helvetica", 10, "bold"), bg="white", fg="#6b7280").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(parent, text="user@stockmaster.com", font=("Helvetica", 10), bg="white", fg="#111827").grid(row=1, column=1, sticky="w", padx=30)

        tk.Label(parent, text="Role:", font=("Helvetica", 10, "bold"), bg="white", fg="#6b7280").grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(parent, text="Administrator", font=("Helvetica", 10), bg="white", fg="#166534").grid(row=2, column=1, sticky="w", padx=30)

        # Action Button
        btn_pass = tk.Button(parent, text="Change Password", font=("Helvetica", 10), 
                             bg="black", fg="white", relief="flat", padx=15, pady=6, cursor="hand2",
                             command=lambda: messagebox.showinfo("Info", "Change Password logic coming soon"))
        btn_pass.grid(row=3, column=0, columnspan=2, sticky="w", pady=(20, 0))

    def prefs_content(self, parent):
        """Content for Preferences Card"""
        # Theme Dropdown
        tk.Label(parent, text="Visual Theme:", font=("Helvetica", 10), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        combo_theme = ttk.Combobox(parent, values=["Light Mode", "Dark Mode"], state="readonly", font=("Helvetica", 10))
        combo_theme.set("Light Mode")
        combo_theme.grid(row=0, column=1, padx=30, sticky="w")

        # Notification Toggle
        tk.Label(parent, text="Email Alerts:", font=("Helvetica", 10), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        
        self.var_notify = tk.BooleanVar(value=True)
        chk_notify = tk.Checkbutton(parent, text="Receive Low Stock Alerts", variable=self.var_notify, 
                                    bg="white", activebackground="white", font=("Helvetica", 10))
        chk_notify.grid(row=1, column=1, padx=25, sticky="w")

        # Save Button
        btn_save = tk.Button(parent, text="Save Preferences", font=("Helvetica", 10, "bold"), 
                             bg="#2563eb", fg="white", relief="flat", padx=15, pady=6, cursor="hand2",
                             command=lambda: messagebox.showinfo("Info", "Preferences Saved locally"))
        btn_save.grid(row=2, column=0, columnspan=2, sticky="w", pady=(20, 0))

    def about_content(self, parent):
        """Content for System Info"""
        tk.Label(parent, text="Stock Master v1.0.0", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(parent, text="Developed for Inventory Management Module 1.", font=("Helvetica", 10), fg="#6b7280", bg="white").pack(anchor="w", pady=(2, 10))
        
        btn_update = tk.Button(parent, text="Check for Updates", font=("Helvetica", 9), 
                               bg="#f3f4f6", fg="#374151", relief="flat", padx=10, pady=4,
                               command=lambda: messagebox.showinfo("Update", "You are on the latest version."))
        btn_update.pack(anchor="w")