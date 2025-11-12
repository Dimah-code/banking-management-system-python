import tkinter as tk
from gui.widgets import BaseContentFrame, AdminSidebar

class AdminDashboardFrame(BaseContentFrame):
    """Main dashboard frame for admin users with sidebar"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, AdminSidebar)
        self._setup_sub_frames()

    def _setup_sub_frames(self):
        """Setup all admin sub-frames"""
        from .admin_overview import AdminOverviewFrame
        from .admin_accounts import AdminAccountsFrame
        from .admin_statement import AdminStatementFrame

        self.add_sub_frame("AdminOverviewFrame", AdminOverviewFrame)
        self.add_sub_frame("AdminAccountsFrame", AdminAccountsFrame)
        self.add_sub_frame("AdminStatementFrame", AdminStatementFrame)

    def on_show(self):
        """Called when admin dashboard is displayed"""
        super().on_show()