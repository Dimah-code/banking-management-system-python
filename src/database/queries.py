# src/database/queries.py

# ==================== TABLE CREATION QUERIES ====================

ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.00
)
"""

TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    type TEXT NOT NULL, 
    amount REAL NOT NULL,
    timestamp TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
)
"""

ADMINS_TABLE = """
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
"""

# ==================== ADMIN QUERIES ====================

FIND_ADMIN_BY_USERNAME = "SELECT id FROM admins WHERE username=?"
CREATE_DEFAULT_ADMIN = "INSERT INTO admins (username, password) VALUES (?, ?)"
CHECK_ADMIN_CREDENTIALS = "SELECT id FROM admins WHERE username=? AND password=?"

# ==================== TRANSACTION QUERIES ====================

SELECT_ALL_TRANSACTIONS = "SELECT COUNT(*) FROM transactions"
INSERT_TRANSACTION = """
INSERT INTO transactions (account_id, type, amount, timestamp, description)
VALUES (?, ?, ?, ?, ?)
"""
UPDATE_BALANCE_DEPOSIT = "UPDATE accounts SET balance = balance + ? WHERE id=?"
UPDATE_BALANCE_WITHDRAW = "UPDATE accounts SET balance = balance - ? WHERE id=?"
GET_TRANSACTION = """
SELECT timestamp, type, amount, description FROM transactions 
WHERE account_id=? ORDER BY timestamp DESC
"""

RECORD_TRANACTION = """
INSERT INTO transactions (account_id, type, amount, timestamp, description) 
VALUES (?, ?, ?, ?, ?)
"""

GET_ALL_TRANSACTIONS = """
SELECT 
    t.timestamp, 
    a.username, 
    t.type, 
    t.amount, 
    t.description 
FROM transactions t
JOIN accounts a ON t.account_id = a.id
ORDER BY t.timestamp DESC
"""

# ==================== ACCOUNT QUERIES ====================

CHECK_USER_CREDENTIALS = "SELECT id, username FROM accounts WHERE username=? AND password=?"
CREATE_ACCOUNT = "INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)"
GET_BALANCE = "SELECT balance FROM accounts WHERE id=?"
GET_ACCOUNT_ID = "SELECT id FROM accounts WHERE username=?"
UPDATE_BALANCE = "UPDATE accounts SET balance = balance + ? WHERE id=?"
GET_ALL_SUMMARIES = "SELECT id, username, balance FROM accounts ORDER BY id ASC"