import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *
from utils.validators import validate_amount

class TransferFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup transfer form UI"""
        transfer_container = tk.Frame(self, bg=BG_PRIMARY, padx=50, pady=30)
        transfer_container.pack(fill="both", expand=True)

        tk.Label(transfer_container, text="Transfer Funds", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=ACCENT_BLUE).pack(pady=(10, 30))

        # Recipient field
        tk.Label(transfer_container, text="Recipient Username:", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=5)
        self.recipient_entry = ttk.Entry(transfer_container, width=30, justify='center')
        self.recipient_entry.pack(pady=5, ipadx=20)
        
        # Amount field
        tk.Label(transfer_container, text="Amount ($):", font=HEADER_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=5)
        self.amount_entry = ttk.Entry(transfer_container, width=30, justify='center')
        self.amount_entry.pack(pady=10, ipadx=20)

        transfer_btn = ttk.Button(transfer_container, text="Confirm Transfer", 
                                style='Action.TButton', command=self._handle_transfer)
        transfer_btn.pack(pady=30, ipadx=50)

    def _handle_transfer(self):
        """Handle transfer transaction"""
        recipient_username = self.recipient_entry.get().strip()
        
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Transfer amount must be positive.")
            return

        sender_id = self.controller.current_user_id
        sender_username = self.controller.current_username
        
        recipient_id = self.controller.db.get_account_id_by_username(recipient_username)
        
        if recipient_id is None:
            messagebox.showerror("Transfer Failed", f"Recipient account '{recipient_username}' not found.")
            return
            
        if sender_id == recipient_id:
            messagebox.showerror("Transfer Failed", "Cannot transfer funds to your own account.")
            return

        current_balance = self.controller.db.get_balance(sender_id)

        if amount > current_balance:
            messagebox.showerror("Insufficient Funds", 
                               f"You only have ${current_balance:,.2f} in your account.")
            return

        try:
            self.controller.db.update_balance(sender_id, -amount)
            self.controller.db.update_balance(recipient_id, amount)
            self.controller.db.record_transaction(sender_id, 'Transfer (Out)', -amount, 
                                                f"Transfer to {recipient_username}")
            self.controller.db.record_transaction(recipient_id, 'Transfer (In)', amount, 
                                                f"Transfer from {sender_username}")

            self.controller.frames["UserHomeFrame"].sub_frames["AccountSummaryFrame"]._update_balance_display()
            messagebox.showinfo("Success", f"Successfully transferred ${amount:,.2f} to {recipient_username}.")
            self._on_hide()
            self.controller.frames["UserHomeFrame"].show_sub_frame("AccountSummaryFrame")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transfer: {e}")

    def on_show(self):
        """Called when frame is displayed"""
        self._clear_fields()
        self.recipient_entry.focus_set()

    def _on_hide(self):
        """Called when frame is hidden"""
        self._clear_fields()
        
    def _clear_fields(self):
        """Clear all input fields"""
        self.recipient_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)