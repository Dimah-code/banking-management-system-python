import tkinter as tk
from config.settings import *

class AdminOverviewFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup admin overview dashboard UI"""
        # Title
        tk.Label(self, text="Admin Dashboard", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=ADMIN_COLOR).pack(pady=(10, 20))
        
        # Statistics section
        tk.Label(self, text="System Statistics", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=10)
        
        # Stats container
        stats_frame = tk.Frame(self, bg=BG_DARK, padx=30, pady=30)
        stats_frame.pack(pady=20, padx=50, fill="x")
        
        # Total accounts
        self.total_accounts_label = tk.Label(stats_frame, text="Total Accounts: N/A", 
                                           font=HEADER_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT)
        self.total_accounts_label.pack(pady=5)
        
        # Total balance
        self.total_balance_label = tk.Label(stats_frame, text="Total Balance: N/A", 
                                          font=HEADER_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT)
        self.total_balance_label.pack(pady=5)
        
        # Info text
        tk.Label(stats_frame, text="View 'Accounts' and 'Full Statement' for detailed data.", 
                font=FONT_STYLE, bg=BG_DARK, fg=ACCENT_BLUE).pack(pady=20)

    def on_show(self):
        """Update statistics when frame is shown"""
        self._update_statistics()

    def _update_statistics(self):
        """Fetch and display system statistics"""
        all_accounts = self.controller.db.get_all_accounts_summary()
        
        total_accounts = len(all_accounts)
        total_balance = sum(balance for _, _, balance in all_accounts)
        
        self.total_accounts_label.config(text=f"Total Accounts: {total_accounts}")
        self.total_balance_label.config(text=f"Total System Balance: ${total_balance:,.2f}")