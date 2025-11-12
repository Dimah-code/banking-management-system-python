import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup login form UI"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        
        # Title
        tk.Label(self, text="Account Login", font=TITLE_FONT_STYLE, 
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

        # Buttons
        login_btn = ttk.Button(self, text="Login", style='T.TButton', 
                             command=self._login_user)
        login_btn.grid(row=4, column=0, columnspan=2, pady=(30, 10), ipadx=50)

        back_btn = ttk.Button(self, text="Back to Welcome", style='T.TButton', 
                            command=lambda: self.controller.show_frame("WelcomeFrame"))
        back_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=50)

    def _login_user(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        result = self.controller.db.check_credentials(username, password)

        if result:
            user_id, uname = result
            messagebox.showinfo("Success", f"Welcome, {uname}!")
            self._clear_fields()
            self.controller.login(user_id, uname)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def _clear_fields(self):
        """Clear input fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def on_show(self):
        """Called when frame is displayed"""
        self._clear_fields()
        self.username_entry.focus_set()