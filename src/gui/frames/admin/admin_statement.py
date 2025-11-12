import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import *
from utils.sorting import merge_sort

class AdminStatementFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_PRIMARY)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        """Setup admin statement view UI"""
        statement_container = tk.Frame(self, bg=BG_PRIMARY, padx=20, pady=20)
        statement_container.pack(fill="both", expand=True)
        
        # Title
        tk.Label(statement_container, text="Full System Transaction History", 
                font=TITLE_FONT_STYLE, bg=BG_PRIMARY, fg=FG_LIGHT).pack(pady=(10, 20))
        
        # Treeview container
        tree_frame = tk.Frame(statement_container, bg=BG_PRIMARY)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview setup
        columns = ("Timestamp", "User", "Type", "Amount", "Description")
        self.statement_tree = ttk.Treeview(tree_frame, columns=columns, 
                                         show="headings", height=15)
        
        self.statement_tree.heading("Timestamp", text="Date/Time")
        self.statement_tree.heading("User", text="User")
        self.statement_tree.heading("Type", text="Type")
        self.statement_tree.heading("Amount", text="Amount")
        self.statement_tree.heading("Description", text="Description")
        
        self.statement_tree.column("Timestamp", width=120, anchor="center")
        self.statement_tree.column("User", width=100, anchor="center")
        self.statement_tree.column("Type", width=100, anchor="center")
        self.statement_tree.column("Amount", width=90, anchor="e")
        self.statement_tree.column("Description", width=200, anchor="w")
        
        # Scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", 
                          command=self.statement_tree.yview)
        vsb.pack(side="right", fill="y")
        self.statement_tree.configure(yscrollcommand=vsb.set)
        
        self.statement_tree.pack(side="left", fill="both", expand=True)

        # Export button
        ttk.Button(statement_container, text="Export to CSV 📄", style='Admin.TButton', 
                 command=self._export_data).pack(pady=10, ipadx=50)

    def _export_data(self):
        """Export transaction data to CSV"""
        try:
            filename = self.controller.db.export_all_transactions_to_csv()
            
            if filename:
                messagebox.showinfo("Export Successful", 
                                  f"Successfully exported all transactions to:\n{filename}")
            else:
                messagebox.showwarning("Export Warning", "No transaction data found to export.")

        except IOError as e:
            messagebox.showerror("Export Failed", f"A file system error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An unexpected error occurred during export: {e}")
        
    def on_show(self):
        """Refresh transaction history when frame is shown"""
        self._refresh_transactions()

    def _refresh_transactions(self):
        """Refresh and display all system transactions"""
        # Clear existing entries
        for item in self.statement_tree.get_children():
            self.statement_tree.delete(item)
            
        # Use cached sorted transactions or fetch new
        if getattr(self.controller, 'sorted_all_transactions', None) is not None:
            sorted_history = self.controller.sorted_all_transactions
        else:
            history = self.controller.db.get_all_transactions()

            if not history:
                self.statement_tree.insert("", "end", 
                                         values=("---", "---", "No System Transactions", "---", "---"))
                return

            try:
                sorted_history = merge_sort(history, key_index=0, ascending=False)
            except Exception:
                sorted_history = history

        # Populate treeview
        for record in sorted_history:
            timestamp, username, type, amount, description = record
            
            # Format amount with color coding
            if amount > 0:
                formatted_amount = f"${amount:,.2f}"
                tag = 'green'
            else:
                formatted_amount = f"-${abs(amount):,.2f}"
                tag = 'red'

            self.statement_tree.insert("", "end", 
                                     values=(timestamp, username, type, formatted_amount, description), 
                                     tags=(tag,))
            
        # Configure colors
        try:
            self.statement_tree.tag_configure('green', foreground=SUCCESS_GREEN)
            self.statement_tree.tag_configure('red', foreground=WARNING_RED)
        except Exception:
            pass