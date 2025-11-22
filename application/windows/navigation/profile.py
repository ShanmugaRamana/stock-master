import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ProfileView:
    def __init__(self, parent, dashboard=None):
        self.parent = parent
        self.dashboard = dashboard
        self.API_URL = "http://127.0.0.1:8000"
        
        self.frame = tk.Frame(parent, bg="#f3f4f6")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.setup_header()
        self.setup_content()

    def setup_header(self):
        header_frame = tk.Frame(self.frame, bg="#f3f4f6")
        header_frame.pack(fill="x", pady=(0, 20))
        
        btn_back = tk.Button(header_frame, text="← Back to Overview", font=("Helvetica", 10, "bold"), 
                             bg="#e5e7eb", fg="#374151", relief="flat", cursor="hand2", padx=15, pady=6,
                             command=self.go_back)
        btn_back.pack(side="left", padx=(0, 15))
        
        tk.Label(header_frame, text="User Profile", font=("Helvetica", 24, "bold"), fg="#111827", bg="#f3f4f6").pack(side="left")

    def setup_content(self):
        self.content_frame = tk.Frame(self.frame, bg="#f3f4f6")
        self.content_frame.pack(fill="both", expand=True)
        
        # Left Column
        left_frame = tk.Frame(self.content_frame, bg="#f3f4f6")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.create_info_card(left_frame)
        
        # Right Column
        right_frame = tk.Frame(self.content_frame, bg="#f3f4f6")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.create_security_card(right_frame)

    def create_info_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=30, pady=30, relief="flat")
        card.pack(fill="x", anchor="n")
        
        tk.Label(card, text="Personal Information", font=("Helvetica", 14, "bold"), bg="white", fg="#111827").pack(anchor="w", pady=(0, 20))
        
        tk.Label(card, text="👤", font=("Arial", 50), bg="white", fg="#3b82f6").pack(anchor="center", pady=(0, 10))
        
        username = self.dashboard.user_details.get('username', 'User') if self.dashboard else "User"
        email = self.dashboard.user_details.get('email', 'N/A') if self.dashboard else "N/A"
        user_id = str(self.dashboard.user_details.get('user_id', 'N/A')) if self.dashboard else "N/A"
        
        tk.Label(card, text=username, font=("Helvetica", 18, "bold"), bg="white", fg="#111827").pack(anchor="center")
        tk.Label(card, text=email, font=("Helvetica", 10), bg="white", fg="#6b7280").pack(anchor="center", pady=(0, 20))
        
        ttk.Separator(card, orient='horizontal').pack(fill='x', pady=15)
        
        self.create_display_field(card, "Role", "Administrator")
        self.create_display_field(card, "Account ID", user_id)
        self.create_display_field(card, "Status", "Active ✅")

    def create_security_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=30, pady=30, relief="flat")
        card.pack(fill="x", anchor="n")
        
        tk.Label(card, text="Security Settings", font=("Helvetica", 14, "bold"), bg="white", fg="#111827").pack(anchor="w", pady=(0, 20))
        
        self.entry_curr_pass = self.create_input(card, "Current Password", "", is_pass=True)
        self.entry_new_pass = self.create_input(card, "New Password", "", is_pass=True)
        self.entry_conf_pass = self.create_input(card, "Confirm New Password", "", is_pass=True)
        
        btn_save = tk.Button(card, text="Update Password", bg="#1f2937", fg="white", font=("Helvetica", 10, "bold"), 
                             relief="flat", pady=10, cursor="hand2",
                             command=self.handle_password_update)
        btn_save.pack(fill="x", pady=(20, 0))

    def handle_password_update(self):
        curr = self.entry_curr_pass.get()
        new = self.entry_new_pass.get()
        conf = self.entry_conf_pass.get()
        
        # Validation
        if not curr or not new or not conf:
            messagebox.showwarning("Missing Input", "Please fill all password fields.")
            return
        if new != conf:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        if len(new) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return

        login_id = self.dashboard.user_details.get('username')
        if not login_id: return

        payload = {
            "login_id": login_id,
            "current_password": curr,
            "new_password": new
        }

        try:
            res = requests.post(f"{self.API_URL}/update-password", json=payload)
            if res.status_code == 200:
                self.show_success_screen()
            else:
                err = res.json().get("detail", "Update failed")
                messagebox.showerror("Error", err)
        except:
            messagebox.showerror("Error", "Server Connection Failed")

    def show_success_screen(self):
        # Clear the entire profile frame content
        for widget in self.frame.winfo_children():
            widget.destroy()

        success_frame = tk.Frame(self.frame, bg="#f3f4f6")
        success_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Draw Tick Mark Canvas
        tick_canvas = tk.Canvas(success_frame, width=120, height=120, bg="#f3f4f6", highlightthickness=0)
        tick_canvas.pack(pady=(0, 20))
        
        color_success = "#10B981"
        # Draw Circle
        tick_canvas.create_oval(10, 10, 110, 110, outline=color_success, width=5)
        # Draw Tick
        tick_canvas.create_line(30, 60, 55, 85, fill=color_success, width=6, capstyle="round")
        tick_canvas.create_line(55, 85, 90, 40, fill=color_success, width=6, capstyle="round")

        tk.Label(success_frame, text="Password Changed Successfully!", font=("Helvetica", 22, "bold"), fg="#111827", bg="#f3f4f6").pack()
        tk.Label(success_frame, text="Redirecting to Login in 5 seconds...", font=("Helvetica", 12), fg="#6b7280", bg="#f3f4f6").pack(pady=10)

        # Schedule Redirect
        self.frame.after(5000, self.logout_to_login)

    def logout_to_login(self):
        # Close dashboard and open login (using dashboard's method usually, or importing)
        from windows.login import LoginScreen
        # We need the root window. Since self.parent is content_frame's parent (dashboard frame), 
        # we usually need self.dashboard.root or similar. 
        # Assuming self.dashboard.root is available:
        root = self.dashboard.root
        # Clear root
        for widget in root.winfo_children():
            widget.destroy()
        # Reset geometry (optional, login handles it)
        LoginScreen(root)

    def create_display_field(self, parent, label, value):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=label, font=("Helvetica", 10, "bold"), bg="white", fg="#6b7280").pack(side="left")
        tk.Label(frame, text=value, font=("Helvetica", 10), bg="white", fg="#111827").pack(side="right")

    def create_input(self, parent, label, value, is_pass=False):
        tk.Label(parent, text=label, font=("Helvetica", 9, "bold"), bg="white", fg="#6b7280").pack(anchor="w", pady=(10, 2))
        entry = tk.Entry(parent, font=("Helvetica", 11), relief="solid", bd=1, bg="white", show="*" if is_pass else "")
        entry.insert(0, value)
        entry.pack(fill="x", ipady=5)
        return entry

    def go_back(self):
        from windows.navigation.overview import OverviewView
        if self.dashboard:
            self.dashboard.load_view("Overview", OverviewView)