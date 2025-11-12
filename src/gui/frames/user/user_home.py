import tkinter as tk
from gui.widgets import BaseContentFrame, UserSidebar

class UserHomeFrame(BaseContentFrame):
    """Main home frame for regular users with sidebar"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, UserSidebar)
        self._setup_sub_frames()

    def _setup_sub_frames(self):
        """Setup all user sub-frames"""
        from .account_summary import AccountSummaryFrame
        from .deposit_frame import DepositFrame
        from .withdraw_frame import WithdrawFrame
        from .transfer_frame import TransferFrame
        from .statement_frame import StatementFrame

        self.add_sub_frame("AccountSummaryFrame", AccountSummaryFrame)
        self.add_sub_frame("DepositFrame", DepositFrame)
        self.add_sub_frame("WithdrawFrame", WithdrawFrame)
        self.add_sub_frame("TransferFrame", TransferFrame)
        self.add_sub_frame("StatementFrame", StatementFrame)

    def on_show(self):
        """Called when user home is displayed"""
        super().on_show()