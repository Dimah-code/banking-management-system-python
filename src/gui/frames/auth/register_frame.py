import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *
from utils.validators import validate_amount, validate_username

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup registration form UI"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)

        # Title
        tk.Label(self, text="Create New Account", font=TITLE_FONT_STYLE, 
                bg=BG_DARK, fg=FG_LIGHT).grid(row=1, column=0, columnspan=2, pady=(40, 30))

        # Username field
        tk.Label(self, text="Username:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, 
                anchor="w").grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self, width=40)
        self.username_entry.grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        # Password field
        tk.Label(self, text="Password:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, 
                anchor="w").grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*", width=40)
        self.password_entry.grid(row=3, column=1, padx=50, pady=10, sticky="ew")
        
        # Initial deposit field
        tk.Label(self, text="Initial Deposit ($):", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, 
                anchor="w").grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.deposit_entry = ttk.Entry(self, width=40)
        self.deposit_entry.grid(row=4, column=1, padx=50, pady=10, sticky="ew")
        self.deposit_entry.insert(0, "0.00")
        
        # Buttons
        register_btn = ttk.Button(self, text="Register", style='T.TButton', 
                                command=self._register_user)
        register_btn.grid(row=5, column=0, columnspan=2, pady=(30, 10), ipadx=50)

        back_btn = ttk.Button(self, text="Back to Welcome", style='T.TButton', 
                            command=lambda: self.controller.show_frame("WelcomeFrame"))
        back_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=50)

    def _register_user(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        initial_deposit = self.deposit_entry.get()

        # Validation
        if not username or not password or not initial_deposit:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate username
        is_valid, username_msg = validate_username(username)
        if not is_valid:
            messagebox.showerror("Invalid Username", username_msg)
            return

        # Validate amount
        is_valid, amount_msg = validate_amount(initial_deposit)
        if not is_valid:
            messagebox.showerror("Invalid Amount", amount_msg)
            return

        # Create account
        result = self.controller.db.create_account(username, password, amount_msg)

        if result is True:
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            self._clear_fields()
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Registration Failed", result)

    def _clear_fields(self):
        """Clear all input fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)
        self.deposit_entry.insert(0, "0.00")

    def on_show(self):
        """Called when frame is displayed"""
        self._clear_fields()
        self.username_entry.focus_set()