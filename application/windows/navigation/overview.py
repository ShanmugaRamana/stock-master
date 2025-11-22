import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class OverviewView:
    def __init__(self, parent):
        self.parent = parent
        self.API_URL = "http://127.0.0.1:8000"
        
        # Main Scrollable Canvas (Optional, but good for dashboards)
        # For simplicity, we use a standard frame first
        self.frame = tk.Frame(parent, bg="#f3f4f6")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.setup_header()
        self.setup_kpi_row()
        self.setup_analytics_section()
        
        self.refresh_data()

    def setup_header(self):
        header_frame = tk.Frame(self.frame, bg="#f3f4f6")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="Dashboard Overview", font=("Helvetica", 24, "bold"), fg="#111827", bg="#f3f4f6").pack(side="left")
        
        # Date Display
        current_date = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(header_frame, text=current_date, font=("Helvetica", 11), fg="#6b7280", bg="#f3f4f6").pack(side="right", pady=5)

    def setup_kpi_row(self):
        """Row of 4 Key Performance Indicators"""
        kpi_frame = tk.Frame(self.frame, bg="#f3f4f6")
        kpi_frame.pack(fill="x", pady=(0, 20))
        
        self.create_kpi_card(kpi_frame, "Total Inventory Value", "₹0.00", "💰", "#2563eb", 0)
        self.create_kpi_card(kpi_frame, "Total Products", "0", "📦", "#10b981", 1)
        self.create_kpi_card(kpi_frame, "Low Stock Alerts", "0", "⚠", "#f59e0b", 2)
        self.create_kpi_card(kpi_frame, "Moves Today", "0", "🚚", "#8b5cf6", 3)

    def create_kpi_card(self, parent, title, value, icon, color, col_index):
        card = tk.Frame(parent, bg="white", padx=20, pady=20, relief="flat")
        card.grid(row=0, column=col_index, sticky="ew", padx=(0, 20)) # Spacing between cards
        parent.grid_columnconfigure(col_index, weight=1)
        
        # Icon (Simulated with Emoji/Text)
        lbl_icon = tk.Label(card, text=icon, font=("Arial", 20), bg="white", fg=color)
        lbl_icon.pack(anchor="w")
        
        # Value
        lbl_val = tk.Label(card, text=value, font=("Helvetica", 22, "bold"), bg="white", fg="#111827")
        lbl_val.pack(anchor="w", pady=(5, 0))
        
        # Title
        lbl_title = tk.Label(card, text=title, font=("Helvetica", 10), bg="white", fg="#6b7280")
        lbl_title.pack(anchor="w")
        
        # Save reference to update later (e.g., self.lbl_val_0)
        setattr(self, f"kpi_val_{col_index}", lbl_val)

    def setup_analytics_section(self):
        """Two main charts side by side"""
        charts_frame = tk.Frame(self.frame, bg="#f3f4f6")
        charts_frame.pack(fill="both", expand=True)
        
        # --- LEFT: Trend Graph ---
        self.left_chart_frame = tk.Frame(charts_frame, bg="white", padx=10, pady=10)
        self.left_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # --- RIGHT: Distribution Graph ---
        self.right_chart_frame = tk.Frame(charts_frame, bg="white", padx=10, pady=10)
        self.right_chart_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

    def refresh_data(self):
        """Fetches data and updates UI"""
        try:
            # 1. Get Products for KPIs
            prod_res = requests.get(f"{self.API_URL}/products")
            products = prod_res.json() if prod_res.status_code == 200 else []
            
            # 2. Get Moves for KPIs
            move_res = requests.get(f"{self.API_URL}/stock-moves")
            moves = move_res.json() if move_res.status_code == 200 else []
            
            # --- CALCULATIONS ---
            total_value = sum(p['stock'] * (p.get('price') or 0) for p in products)
            total_count = len(products)
            low_stock = sum(1 for p in products if 0 < p['stock'] < 10)
            
            today_str = datetime.now().strftime("%Y-%m-%d")
            today_moves = sum(1 for m in moves if m['created_at'].startswith(today_str))
            
            # --- UPDATE UI ---
            self.kpi_val_0.config(text=f"₹{total_value:,.2f}")
            self.kpi_val_1.config(text=str(total_count))
            self.kpi_val_2.config(text=str(low_stock))
            self.kpi_val_3.config(text=str(today_moves))
            
            # --- RENDER CHARTS ---
            self.render_line_chart()
            self.render_bar_chart(products)
            
        except Exception as e:
            print(f"Error loading overview: {e}")

    def render_line_chart(self):
        """Draws a Line Chart (Simulated Trend)"""
        # Clear old
        for w in self.left_chart_frame.winfo_children(): w.destroy()
        
        tk.Label(self.left_chart_frame, text="Inventory Value Trend (Last 7 Days)", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w", pady=10)

        # Simulated Data (Ideally, backend would provide historical snapshots)
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        values = [120000, 125000, 118000, 130000, 135000, 140000, 142000] # Mock data for visuals

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot Line
        ax.plot(days, values, marker='o', color='#2563eb', linewidth=2)
        # Fill area under line
        ax.fill_between(days, values, color='#eff6ff', alpha=0.5)
        
        ax.set_ylim(bottom=100000) # Start y-axis slightly lower than min value
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        canvas = FigureCanvasTkAgg(fig, self.left_chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def render_bar_chart(self, products):
        """Draws a Horizontal Bar Chart of Top Categories by Value"""
        for w in self.right_chart_frame.winfo_children(): w.destroy()
        
        tk.Label(self.right_chart_frame, text="Top Categories by Value", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w", pady=10)

        # Calculate Value per Category
        cat_vals = {}
        for p in products:
            val = p['stock'] * (p.get('price') or 0)
            cat_vals[p['category']] = cat_vals.get(p['category'], 0) + val
            
        # Sort and take top 5
        sorted_cats = sorted(cat_vals.items(), key=lambda x: x[1], reverse=True)[:5]
        if not sorted_cats: return

        cats = [x[0] for x in sorted_cats]
        vals = [x[1] for x in sorted_cats]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Horizontal Bar
        bars = ax.barh(cats, vals, color='#10b981')
        ax.invert_yaxis() # Highest on top
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        canvas = FigureCanvasTkAgg(fig, self.right_chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)