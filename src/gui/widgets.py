import tkinter as tk
from tkinter import ttk
from config.settings import *

class BaseContentFrame(tk.Frame):
    """
    Base class for frames that use sidebar (UserHomeFrame, AdminDashboardFrame)
    """
    def __init__(self, parent, controller, sidebar_class):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self.sidebar_class = sidebar_class
        self._setup_layout()

    def _setup_layout(self):
        """Setup sidebar and content area layout"""
        # Grid setup: Sidebar (25%), Content (75%)
        self.grid_columnconfigure(0, weight=1, minsize=200)  # Sidebar
        self.grid_columnconfigure(1, weight=3)              # Main Content
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Container
        self.sidebar = self.sidebar_class(self, self.controller)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main Content Container
        self.content_container = tk.Frame(self, bg=BG_PRIMARY, padx=20, pady=20)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Initialize sub-frames
        self.sub_frames = {}
        self.current_sub_frame = None
        
    def add_sub_frame(self, name, frame_class):
        """Create and place a sub-frame inside content container"""
        frame = frame_class(self.content_container, self.controller)
        self.sub_frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        return frame

    def show_sub_frame(self, page_name):
        """Raise requested sub-frame and call its on_show method"""
        frame = self.sub_frames.get(page_name)
        if frame:
            # Optional: Call on_hide for current frame
            if self.current_sub_frame and hasattr(self.current_sub_frame, 'on_hide'):
                self.current_sub_frame.on_hide()
                
            frame.tkraise()
            if hasattr(frame, 'on_show'):
                frame.on_show()
            self.current_sub_frame = frame
            
    def on_show(self):
        """Called when the whole main frame is displayed"""
        if hasattr(self.sidebar, 'on_show'):
            self.sidebar.on_show()
        
        # Show first sub-frame by default
        if self.sub_frames:
            first_frame_name = list(self.sub_frames.keys())[0]
            self.show_sub_frame(first_frame_name)


class UserSidebar(tk.Frame):
    """Sidebar for regular users"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=SIDEBAR_COLOR)
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup user sidebar UI"""
        self.columnconfigure(0, weight=1)
        
        # App title
        tk.Label(self, text="Bank App", font=HEADER_FONT_STYLE, 
                bg=SIDEBAR_COLOR, fg=ACCENT_BLUE).grid(row=0, column=0, pady=(30, 20), sticky="n")

        # Navigation buttons
        buttons = {
            "Balance": {"row": 1, "target": "AccountSummaryFrame", "icon": "🏠"},
            "Deposit": {"row": 2, "target": "DepositFrame", "icon": "💰"},
            "Withdraw": {"row": 3, "target": "WithdrawFrame", "icon": "💸"},
            "Transfer": {"row": 4, "target": "TransferFrame", "icon": "📤"},
            "Statement": {"row": 5, "target": "StatementFrame", "icon": "📜"},
        }

        for name, data in buttons.items():
            ttk.Button(self, text=f"{data['icon']} {name}", style='T.TButton',
                     command=lambda t=data['target']: self.master.show_sub_frame(t)) \
                     .grid(row=data['row'], column=0, padx=10, pady=5, sticky="ew")

        # Logout button
        ttk.Button(self, text="Logout", style='Logout.TButton', 
                 command=self.controller.logout) \
                 .grid(row=10, column=0, padx=10, pady=(100, 20), sticky="s")

    def on_show(self):
        """Called when sidebar is displayed"""
        pass


class AdminSidebar(tk.Frame):
    """Sidebar for admin users"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=SIDEBAR_COLOR)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup admin sidebar UI"""
        self.columnconfigure(0, weight=1)
        
        # Admin title
        tk.Label(self, text="Admin Console", font=HEADER_FONT_STYLE, 
                bg=SIDEBAR_COLOR, fg=ADMIN_COLOR).grid(row=0, column=0, pady=(30, 20), sticky="n")

        # Navigation buttons
        buttons = {
            "Dashboard": {"row": 1, "target": "AdminOverviewFrame", "icon": "📊"},
            "Accounts": {"row": 2, "target": "AdminAccountsFrame", "icon": "👤"},
            "Full Statement": {"row": 3, "target": "AdminStatementFrame", "icon": "📋"},
        }
        
        for name, data in buttons.items():
            ttk.Button(self, text=f"{data['icon']} {name}", style='Admin.TButton',
                     command=lambda t=data['target']: self.master.show_sub_frame(t)) \
                     .grid(row=data['row'], column=0, padx=10, pady=5, sticky="ew")

        # Logout button
        ttk.Button(self, text="Admin Logout", style='Logout.TButton', 
                 command=self.controller.logout) \
                 .grid(row=10, column=0, padx=10, pady=(100, 20), sticky="s")

    def on_show(self):
        """Called when sidebar is displayed"""
        pass