import tkinter as tk
from tkinter import ttk
from config.settings import *

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup welcome screen UI"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)

        # Title
        tk.Label(self, text="Secure Banking", font=TITLE_FONT_STYLE, 
                bg=BG_DARK, fg=FG_LIGHT).grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        tk.Label(self, text="Login or Register to access your account.", 
                font=HEADER_FONT_STYLE, bg=BG_DARK, fg=ACCENT_BLUE).grid(
                row=2, column=0, columnspan=2, pady=(10, 40))
        
        # Buttons
        login_btn = ttk.Button(self, text="User Login", style='T.TButton',
                             command=lambda: self.controller.show_frame("LoginFrame"))
        login_btn.grid(row=3, column=0, padx=20, pady=10, ipadx=40, sticky="e")

        register_btn = ttk.Button(self, text="Register", style='T.TButton',
                                command=lambda: self.controller.show_frame("RegisterFrame"))
        register_btn.grid(row=3, column=1, padx=20, pady=10, ipadx=40, sticky="w")
        
        admin_login_btn = ttk.Button(self, text="Admin Login", style='Admin.TButton',
                                   command=lambda: self.controller.show_frame("AdminLoginFrame"))
        admin_login_btn.grid(row=4, column=0, columnspan=2, pady=(20, 10), ipadx=40)
        
        # Footer
        tk.Label(self, text="Powered by Python Tkinter", font=FONT_STYLE, 
                bg=BG_DARK, fg=FG_LIGHT).grid(row=5, column=0, columnspan=2, pady=(80, 0))