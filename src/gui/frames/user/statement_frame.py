import tkinter as tk
from tkinter import ttk
from config.settings import *
from utils.sorting import merge_sort

class StatementFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup statement view UI"""
        statement_container = tk.Frame(self, bg=BG_PRIMARY, padx=20, pady=20)
        statement_container.pack(fill="both", expand=True)
        
        tk.Label(statement_container, text="Account Statement", font=TITLE_FONT_STYLE, 
                bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=(10, 20))
        
        # Treeview setup
        columns = ("Timestamp", "Type", "Amount", "Description")
        self.statement_tree = ttk.Treeview(statement_container, columns=columns, 
                                         show="headings", height=15)
        
        self.statement_tree.heading("Timestamp", text="Date/Time")
        self.statement_tree.heading("Type", text="Type")
        self.statement_tree.heading("Amount", text="Amount")
        self.statement_tree.heading("Description", text="Description")
        
        self.statement_tree.column("Timestamp", width=140, anchor="center")
        self.statement_tree.column("Type", width=100, anchor="center")
        self.statement_tree.column("Amount", width=100, anchor="e")
        self.statement_tree.column("Description", width=200, anchor="w")
        
        vsb = ttk.Scrollbar(statement_container, orient="vertical", 
                          command=self.statement_tree.yview)
        vsb.pack(side="right", fill="y")
        self.statement_tree.configure(yscrollcommand=vsb.set)
        
        self.statement_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
    def on_show(self):
        """Refresh statement data when frame is shown"""
        self._refresh_statement()

    def _refresh_statement(self):
        """Refresh and display transaction statement"""
        # Clear existing entries
        for item in self.statement_tree.get_children():
            self.statement_tree.delete(item)

        user_id = self.controller.current_user_id
        if not user_id:
            return
            
        # Use cached sorted statements or fetch new
        if getattr(self.controller, 'sorted_statements', None) is not None:
            sorted_history = self.controller.sorted_statements
        else:
            history = self.controller.db.get_transaction_history(user_id)
            if not history:
                self.statement_tree.insert("", "end", values=("---", "No Transactions Yet", "---", "---"))
                return

            try:
                sorted_history = merge_sort(history, key_index=0, ascending=False)
            except Exception as e:
                print(f"Sorting error: {e}")
                sorted_history = history

        # Populate treeview
        for record in sorted_history:
            timestamp, type, amount, description = record
            
            # Format amount with color coding
            if amount > 0:
                formatted_amount = f"${amount:,.2f}"
                tag = 'green'
            else:
                formatted_amount = f"-${abs(amount):,.2f}"
                tag = 'red'

            self.statement_tree.insert("", "end", 
                                     values=(timestamp, type, formatted_amount, description), 
                                     tags=(tag,))
            
        # Configure colors
        try:
            self.statement_tree.tag_configure('green', foreground=SUCCESS_GREEN)
            self.statement_tree.tag_configure('red', foreground=WARNING_RED)
        except Exception:
            pass