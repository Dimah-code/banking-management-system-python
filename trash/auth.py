import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import *
from utils.validators import validate_amount, validate_username


class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        
        # Center the content
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)

        tk.Label(self, text="Secure Banking", font=TITLE_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT).grid(row=1, column=0, columnspan=2, pady=(0, 10))
        tk.Label(self, text="Login or Register to access your account.", font=HEADER_FONT_STYLE, bg=BG_DARK, fg=ACCENT_BLUE).grid(row=2, column=0, columnspan=2, pady=(10, 40))
        
        login_btn = ttk.Button(self, text="User Login", style='T.TButton',
                               command=lambda: controller.show_frame("LoginFrame"))
        login_btn.grid(row=3, column=0, padx=20, pady=10, ipadx=40, sticky="e")

        register_btn = ttk.Button(self, text="Register", style='T.TButton',
                                  command=lambda: controller.show_frame("RegisterFrame"))
        register_btn.grid(row=3, column=1, padx=20, pady=10, ipadx=40, sticky="w")
        
        admin_login_btn = ttk.Button(self, text="Admin Login", style='Admin.TButton',
                                     command=lambda: controller.show_frame("AdminLoginFrame"))
        admin_login_btn.grid(row=4, column=0, columnspan=2, pady=(20, 10), ipadx=40)
        
        tk.Label(self, text="Powered by Python Tkinter", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT).grid(row=5, column=0, columnspan=2, pady=(80, 0))


class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)

        tk.Label(self, text="Create New Account", font=TITLE_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT).grid(row=1, column=0, columnspan=2, pady=(40, 30))

        # Input fields
        tk.Label(self, text="Username:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self, width=40)
        self.username_entry.grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        tk.Label(self, text="Password:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*", width=40)
        self.password_entry.grid(row=3, column=1, padx=50, pady=10, sticky="ew")
        
        tk.Label(self, text="Initial Deposit ($):", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.deposit_entry = ttk.Entry(self, width=40)
        self.deposit_entry.grid(row=4, column=1, padx=50, pady=10, sticky="ew")
        self.deposit_entry.insert(0, "0.00")
        
        # Buttons
        register_btn = ttk.Button(self, text="Register", style='T.TButton', command=self.register_user)
        register_btn.grid(row=5, column=0, columnspan=2, pady=(30, 10), ipadx=50)

        back_btn = ttk.Button(self, text="Back to Welcome", style='T.TButton', command=lambda: controller.show_frame("WelcomeFrame"))
        back_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=50)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        initial_deposit = self.deposit_entry.get()

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

        result = self.controller.db.create_account(username, password, amount_msg)

        if result is True:
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            self.clear_fields()
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Registration Failed", result)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)
        self.deposit_entry.insert(0, "0.00")

    def on_show(self):
        self.clear_fields()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        
        tk.Label(self, text="Account Login", font=TITLE_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT).grid(row=1, column=0, columnspan=2, pady=(40, 30))

        # Input fields
        tk.Label(self, text="Username:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self, width=40)
        self.username_entry.grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        tk.Label(self, text="Password:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*", width=40)
        self.password_entry.grid(row=3, column=1, padx=50, pady=10, sticky="ew")

        # Buttons
        login_btn = ttk.Button(self, text="Login", style='T.TButton', command=self.login_user)
        login_btn.grid(row=4, column=0, columnspan=2, pady=(30, 10), ipadx=50)

        back_btn = ttk.Button(self, text="Back to Welcome", style='T.TButton', command=lambda: controller.show_frame("WelcomeFrame"))
        back_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=50)

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        result = self.controller.db.check_credentials(username, password)

        if result:
            user_id, uname = result
            messagebox.showinfo("Success", f"Welcome, {uname}!")
            self.clear_fields()
            self.controller.login(user_id, uname)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()


class AdminLoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        
        tk.Label(self, text="Admin Login", font=TITLE_FONT_STYLE, bg=BG_DARK, fg=ADMIN_COLOR).grid(row=1, column=0, columnspan=2, pady=(40, 30))
        tk.Label(self, text="Access System Management Tools", font=HEADER_FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT).grid(row=2, column=0, columnspan=2, pady=(0, 20))

        # Input fields
        tk.Label(self, text="Admin Username:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self, width=40)
        self.username_entry.grid(row=3, column=1, padx=50, pady=10, sticky="ew")

        tk.Label(self, text="Admin Password:", font=FONT_STYLE, bg=BG_DARK, fg=FG_LIGHT, anchor="w").grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=1, padx=50, pady=10, sticky="ew")

        # Buttons
        login_btn = ttk.Button(self, text="Admin Login", style='Admin.TButton', command=self.login_admin)
        login_btn.grid(row=5, column=0, columnspan=2, pady=(30, 10), ipadx=50)

        back_btn = ttk.Button(self, text="Back to Welcome", style='T.TButton', command=lambda: controller.show_frame("WelcomeFrame"))
        back_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=50)

    def login_admin(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if self.controller.db.check_admin_credentials(username, password):
            messagebox.showinfo("Success", f"Welcome, Admin {username}!")
            self.clear_fields()
            self.controller.login(user_id=0, username=username, is_admin=True) 
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()