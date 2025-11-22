import tkinter as tk
# Import the classes from the windows folder
from windows.splash import SplashScreen
from windows.login import LoginScreen

class StockMasterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Hide main window initially
        self.withdraw()
        
        # Launch Splash Screen
        # Pass 'self.show_login' as the callback for when splash is done
        SplashScreen(self, self.show_login)

    def show_login(self):
        """Callback to show login screen after splash finishes"""
        self.deiconify() # Show the main window
        LoginScreen(self) # Load the login UI into the main window

if __name__ == "__main__":
    app = StockMasterApp()
    app.mainloop()