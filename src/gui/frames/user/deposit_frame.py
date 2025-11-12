import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *
from utils.validators import validate_amount

class DepositFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup deposit form UI"""
        deposit_container = tk.Frame(self, bg=BG_PRIMARY, padx=50, pady=30)
        deposit_container.pack(fill="both", expand=True)

        tk.Label(deposit_container, text="Deposit Money", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=SUCCESS_GREEN).pack(pady=(10, 30))

        tk.Label(deposit_container, text="Amount ($):", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=5)
        
        self.amount_entry = ttk.Entry(deposit_container, width=30, justify='center')
        self.amount_entry.pack(pady=10, ipadx=20)

        deposit_btn = ttk.Button(deposit_container, text="Confirm Deposit", 
                               style='Action.TButton', command=self._handle_deposit)
        deposit_btn.pack(pady=30, ipadx=50)

    def _handle_deposit(self):
        """Handle deposit transaction"""
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Deposit amount must be positive.")
            return

        user_id = self.controller.current_user_id
        
        try:
            self.controller.db.update_balance(user_id, amount)
            self.controller.db.record_transaction(user_id, 'Deposit', amount)

            # Update summary and switch back to it
            self.controller.frames["UserHomeFrame"].sub_frames["AccountSummaryFrame"]._update_balance_display()
            messagebox.showinfo("Success", f"Successfully deposited ${amount:,.2f}.")
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