import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *
from utils.validators import validate_amount

class WithdrawFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup withdraw form UI"""
        withdraw_container = tk.Frame(self, bg=BG_PRIMARY, padx=50, pady=30)
        withdraw_container.pack(fill="both", expand=True)

        tk.Label(withdraw_container, text="Withdraw Money", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=WARNING_RED).pack(pady=(10, 30))

        tk.Label(withdraw_container, text="Amount ($):", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=5)
        
        self.amount_entry = ttk.Entry(withdraw_container, width=30, justify='center')
        self.amount_entry.pack(pady=10, ipadx=20)

        withdraw_btn = ttk.Button(withdraw_container, text="Confirm Withdrawal", 
                                style='Action.TButton', command=self._handle_withdraw)
        withdraw_btn.pack(pady=30, ipadx=50)

    def _handle_withdraw(self):
        """Handle withdrawal transaction"""
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Withdrawal amount must be positive.")
            return

        user_id = self.controller.current_user_id
        current_balance = self.controller.db.get_balance(user_id)

        if amount > current_balance:
            messagebox.showerror("Insufficient Funds", 
                               f"You only have ${current_balance:,.2f} in your account.")
            return

        try:
            self.controller.db.update_balance(user_id, -amount)
            self.controller.db.record_transaction(user_id, 'Withdrawal', -amount)

            self.controller.frames["UserHomeFrame"].sub_frames["AccountSummaryFrame"]._update_balance_display()
            messagebox.showinfo("Success", f"Successfully withdrew ${amount:,.2f}.")
            self._on_hide()
            self.controller.frames["UserHomeFrame"].show_sub_frame("AccountSummaryFrame")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_show(self):
        """Called when frame is displayed"""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.focus_set()

    def _on_hide(self):
        """Called when frame is hidden"""
        self.amount_entry.delete(0, tk.END)