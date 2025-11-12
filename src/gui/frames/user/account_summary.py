import tkinter as tk
from tkinter import ttk
from config.settings import *

class AccountSummaryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup account summary UI"""
        # Title
        tk.Label(self, text="Account Overview", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=(10, 20))

        # Balance display frame
        self.balance_frame = tk.Frame(self, bg=ACCENT_BLUE, padx=40, pady=30, relief="flat")
        self.balance_frame.pack(pady=20, padx=50, fill="x")
        
        tk.Label(self.balance_frame, text="Current Balance:", font=HEADER_FONT_STYLE, 
                 bg=ACCENT_BLUE, fg=BG_DARK).pack()
                 
        self.balance_label = tk.Label(self.balance_frame, text="$0.00", 
                                      font=("Inter", 48, "bold"), bg=ACCENT_BLUE, fg=BG_DARK)
        self.balance_label.pack(pady=10)

        # Quick actions section
        tk.Label(self, text="Quick Actions:", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=ACCENT_BLUE).pack(pady=(30, 10))

        actions_frame = tk.Frame(self, bg=BG_PRIMARY)
        actions_frame.pack(pady=10)
        
        # Quick action buttons
        ttk.Button(actions_frame, text="Deposit", style='Action.TButton', 
                 command=self._go_to_deposit).grid(row=0, column=0, padx=10, pady=10, ipadx=10)
        
        ttk.Button(actions_frame, text="Withdraw", style='Action.TButton', 
                 command=self._go_to_withdraw).grid(row=0, column=1, padx=10, pady=10, ipadx=10)
        
        ttk.Button(actions_frame, text="Transfer", style='Action.TButton', 
                 command=self._go_to_transfer).grid(row=0, column=2, padx=10, pady=10, ipadx=10)

    def _go_to_deposit(self):
        """Navigate to deposit frame"""
        self.controller.frames["UserHomeFrame"].show_sub_frame("DepositFrame")

    def _go_to_withdraw(self):
        """Navigate to withdraw frame"""
        self.controller.frames["UserHomeFrame"].show_sub_frame("WithdrawFrame")

    def _go_to_transfer(self):
        """Navigate to transfer frame"""
        self.controller.frames["UserHomeFrame"].show_sub_frame("TransferFrame")

    def on_show(self):
        """Update balance display when frame is shown"""
        self._update_balance_display()

    def _update_balance_display(self):
        """Fetch and display updated balance"""
        if not self.controller.current_user_id:
            return
            
        balance = self.controller.db.get_balance(self.controller.current_user_id)
        self.balance_label.config(text=f"${balance:,.2f}")