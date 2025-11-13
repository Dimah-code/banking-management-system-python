import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import *
from database.manager import DatabaseManager
from utils.sorting import merge_sort

# Import frames using absolute imports
from gui.frames.auth.welcome_frame import WelcomeFrame
from gui.frames.auth.register_frame import RegisterFrame
from gui.frames.auth.login_frame import LoginFrame
from gui.frames.auth.admin_login_frame import AdminLoginFrame
from gui.frames.user.user_home import UserHomeFrame
from gui.frames.admin.admin_dashboard import AdminDashboardFrame

# Import widgets
from gui.widgets import BaseContentFrame
from gui.widgets import UserSidebar, AdminSidebar



class BankingApp(tk.Tk):
    """
    Main application window and controller. 
    Manages frames (views) and holds the DatabaseManager instance.
    """
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)  # ← CHANGE THIS LINE
            self.title(APP_NAME)
            self.geometry("1000x650")
            self.resizable(False, False)
            self.config(bg=BG_DARK)

            try:
                self.db = DatabaseManager()
            except Exception as e:
                messagebox.showerror("Database Startup Error", f"Failed to initialize database: {str(e)}")
                self.destroy()  # Use destroy instead of quit
                return  # Stop initialization if database fails

            self._setup_styles()
            self._setup_ui()
            self._reset_session()


    def _setup_styles(self):
        """Configure modern Tkinter styles for improved UX"""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # General Styles
        style.configure('.', font=FONT_STYLE, background=BG_PRIMARY, foreground=FG_LIGHT)
        style.configure('TFrame', background=BG_PRIMARY)
        style.configure('TLabel', background=BG_PRIMARY, foreground=FG_LIGHT)
        style.configure('TEntry', fieldbackground=BG_DARK, foreground=FG_LIGHT, borderwidth=1, relief="flat", padding=5)
        
        # Button styles
        style.configure('T.TButton', font=BUTTON_FONT_STYLE, padding=[20, 10], 
                        background=ACCENT_BLUE, foreground=FG_LIGHT, borderwidth=0, relief="flat")
        style.map('T.TButton', background=[('active', '#1a3d7a')], foreground=[('active', FG_LIGHT)])

        style.configure('Action.TButton', font=BUTTON_FONT_STYLE, padding=[15, 8], 
                        background=SUCCESS_GREEN, foreground=BG_DARK, borderwidth=0, relief="flat")
        style.map('Action.TButton', background=[('active', '#3bbd60')], foreground=[('active', BG_DARK)])
        
        style.configure('Logout.TButton', font=BUTTON_FONT_STYLE, padding=[15, 8], 
                        background=WARNING_RED, foreground=FG_LIGHT, borderwidth=0, relief="flat")
        style.map('Logout.TButton', background=[('active', '#e55c5c')], foreground=[('active', FG_LIGHT)])
        
        style.configure('Admin.TButton', font=BUTTON_FONT_STYLE, padding=[15, 8], 
                        background=ADMIN_COLOR, foreground=BG_DARK, borderwidth=0, relief="flat")
        style.map('Admin.TButton', background=[('active', '#f5a623')], foreground=[('active', BG_DARK)])
        
        # Treeview styling
        style.configure("Treeview.Heading", font=FONT_STYLE, background=SIDEBAR_COLOR, foreground=FG_LIGHT, padding=5)
        style.configure("Treeview", background=BG_PRIMARY, foreground=FG_LIGHT, fieldbackground=BG_PRIMARY, rowheight=25)


    def _setup_ui(self):
        """Setup the main UI container and frames"""
        # Container setup for frames
        self._container = tk.Frame(self, bg=BG_DARK)  # Make it instance variable
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Define all available frames
        for F in (WelcomeFrame, RegisterFrame, LoginFrame, AdminLoginFrame, UserHomeFrame, AdminDashboardFrame):
            page_name = F.__name__
            frame = F(parent=self._container, controller=self)  # Pass self (BankingApp)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeFrame")


    def _reset_session(self):
        """Reset user session data"""
        self.current_user_id = None
        self.current_username = None
        self.is_admin = False
        self.sorted_statements = None
        self.sorted_accounts = None
        self.sorted_all_transactions = None

    def show_frame(self, page_name):
        """Raises the requested frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def login(self, user_id, username, is_admin=False):
        """Sets the current user state after successful login."""
        self.current_user_id = user_id
        self.current_username = username
        self.is_admin = is_admin
        
        # Pre-fetch data for better performance
        self._prefetch_data()
        
        if is_admin:
            self.show_frame("AdminDashboardFrame")
        else:
            self.show_frame("UserHomeFrame")

    def _prefetch_data(self):
        """Prefetch and cache data for better performance"""
        if not self.is_admin and self.current_user_id:
            try:
                self._prefetch_user_statements()
            except Exception:
                self.sorted_statements = None

        if self.is_admin:
            try:
                self._prefetch_admin_data()
            except Exception:
                self.sorted_accounts = None
                self.sorted_all_transactions = None

    def _prefetch_user_statements(self):
        """Prefetch and sort user transaction history"""
        history = self.db.get_transaction_history(self.current_user_id)
        if history:
            try:
                self.sorted_statements = merge_sort(history, key_index=0, ascending=False)
            except Exception:
                self.sorted_statements = history

    def _prefetch_admin_data(self):
        """Prefetch and sort admin data"""
        # Accounts data
        all_accounts = self.db.get_all_accounts_summary()
        if all_accounts:
            try:
                self.sorted_accounts = merge_sort(all_accounts, key_index=1, ascending=True)
            except Exception:
                self.sorted_accounts = all_accounts

        # All transactions
        history = self.db.get_all_transactions()
        if history:
            try:
                self.sorted_all_transactions = merge_sort(history, key_index=0, ascending=False)
            except Exception:
                self.sorted_all_transactions = history

    def logout(self):
        """Resets user state and returns to welcome screen."""
        self._reset_session()
        self.show_frame("WelcomeFrame")