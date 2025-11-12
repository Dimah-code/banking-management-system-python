import tkinter as tk
from tkinter import ttk
from config.settings import *
from utils.sorting import merge_sort

class AdminAccountsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup admin accounts view UI"""
        accounts_container = tk.Frame(self, bg=BG_PRIMARY, padx=20, pady=20)
        accounts_container.pack(fill="both", expand=True)
        
        # Title
        tk.Label(accounts_container, text="All Client Accounts", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=(10, 20))
        
        # Treeview setup
        columns = ("ID", "Username", "Balance")
        self.accounts_tree = ttk.Treeview(accounts_container, columns=columns, 
                                        show="headings", height=15)
        
        self.accounts_tree.heading("ID", text="ID")
        self.accounts_tree.heading("Username", text="Username")
        self.accounts_tree.heading("Balance", text="Balance")
        
        self.accounts_tree.column("ID", width=50, anchor="center")
        self.accounts_tree.column("Username", width=150, anchor="center")
        self.accounts_tree.column("Balance", width=150, anchor="e")
        
        # Scrollbar
        vsb = ttk.Scrollbar(accounts_container, orient="vertical", 
                          command=self.accounts_tree.yview)
        vsb.pack(side="right", fill="y")
        self.accounts_tree.configure(yscrollcommand=vsb.set)
        
        self.accounts_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
    def on_show(self):
        """Refresh accounts data when frame is shown"""
        self._refresh_accounts()

    def _refresh_accounts(self):
        """Refresh and display all user accounts"""
        # Clear existing entries
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)

        # Use cached sorted accounts or fetch new
        if getattr(self.controller, 'sorted_accounts', None) is not None:
            all_accounts = self.controller.sorted_accounts
        else:
            all_accounts = self.controller.db.get_all_accounts_summary()
            try:
                # Sort by username alphabetically
                all_accounts = merge_sort(all_accounts, key_index=1, ascending=True)
            except Exception:
                # Fall back to DB order
                pass

        if not all_accounts:
            self.accounts_tree.insert("", "end", values=("---", "No User Accounts Found", "---"))
            return

        # Populate treeview
        for acc_id, username, balance in all_accounts:
            formatted_balance = f"${balance:,.2f}"
            self.accounts_tree.insert("", "end", values=(acc_id, username, formatted_balance))