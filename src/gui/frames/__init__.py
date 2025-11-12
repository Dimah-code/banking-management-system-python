from .auth import WelcomeFrame, LoginFrame, RegisterFrame, AdminLoginFrame
from .user import UserHomeFrame, AccountSummaryFrame, DepositFrame, WithdrawFrame, TransferFrame, StatementFrame
from .admin import AdminDashboardFrame, AdminOverviewFrame, AdminAccountsFrame, AdminStatementFrame

__all__ = [
    'WelcomeFrame', 'LoginFrame', 'RegisterFrame', 'AdminLoginFrame',
    'UserHomeFrame', 'AccountSummaryFrame', 'DepositFrame', 'WithdrawFrame', 
    'TransferFrame', 'StatementFrame',
    'AdminDashboardFrame', 'AdminOverviewFrame', 'AdminAccountsFrame', 'AdminStatementFrame'
]