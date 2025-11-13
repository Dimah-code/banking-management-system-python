import sqlite3
import csv
import os
from datetime import datetime
from typing import Optional, Tuple, List, Union
from config.settings import (
    DATABASE_NAME, ADMIN_USERNAME, ADMIN_PASSWORD, 
    CSV_EXPORT_FILENAME, INITIAL_ACCOUNTS_FILE, DATABASE_PATH
)


class DatabaseManager:
    """
    Manages all persistent data operations for the banking application using SQLite.
    This class follows Single Responsibility Principle with clear separation of concerns.
    """
    
    def __init__(self):
        """Initializes the database connection and creates necessary tables."""
        self.db_conn = self._connect_db()
        self._initialize_database()
        self._load_initial_data()

    # ==================== DATABASE INITIALIZATION ====================
    
    def _connect_db(self) -> sqlite3.Connection:
        """Establish database connection with error handling."""
        try:
            return sqlite3.connect(DATABASE_PATH)
        except sqlite3.Error as e:
            raise ConnectionError(f"Database connection failed: {e}")

    def _initialize_database(self):
        """Create all necessary tables and default admin account."""
        schema_scripts = [
            # Accounts Table
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.00
            )
            """,
            # Transactions Table
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                type TEXT NOT NULL, 
                amount REAL NOT NULL,
                timestamp TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            )
            """,
            # Admins Table
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        ]
        
        cursor = self.db_conn.cursor()
        try:
            for script in schema_scripts:
                cursor.execute(script)
            
            self._create_default_admin()
            self.db_conn.commit()
            
        except sqlite3.Error as e:
            raise ConnectionError(f"Database initialization failed: {e}")

    def _create_default_admin(self):
        """Create default admin account if it doesn't exist."""
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("SELECT id FROM admins WHERE username=?", (ADMIN_USERNAME,))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (?, ?)", 
                    (ADMIN_USERNAME, ADMIN_PASSWORD)
                )
                self.db_conn.commit()
                print("✅ Default admin account created successfully")
        except sqlite3.Error as e:
            print(f"❌ Error creating default admin: {e}")
            # Don't raise the error, just log it

    # ==================== INITIAL DATA LOADING ====================
    
    def _load_initial_data(self):
        """Import transaction data from CSV if database is empty."""
        if self._has_existing_data():
            print("✅ Transactions already exist in DB — skipping CSV load.")
            return
        
        print("Loading data from system_transactions.csv...")
        self._import_transactions_from_csv()

    def _has_existing_data(self) -> bool:
        """Check if transactions table already has data."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions")
        return cursor.fetchone()[0] > 0

    def _import_transactions_from_csv(self):
        """Import transactions from CSV file with validation."""
        if not os.path.exists(INITIAL_ACCOUNTS_FILE):
            print(f"⚠ CSV file not found: {INITIAL_ACCOUNTS_FILE}")
            return

        try:
            with open(INITIAL_ACCOUNTS_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self._process_csv_data(reader)
                
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")

    def _process_csv_data(self, reader):
        """Process and validate each row in the CSV data."""
        required_fields = {"Username", "Type", "Amount"}
        if not required_fields.issubset(reader.fieldnames):
            print("⚠ CSV file format not supported. Expected headers: Username, Type, Amount, Description, Timestamp")
            return

        for row in reader:
            self._process_transaction_row(row)

        self.db_conn.commit()
        print("✅ Transaction CSV import complete.")

    def _process_transaction_row(self, row: dict):
        """Process a single transaction row from CSV."""
        username = row.get("Username", "").strip()
        tx_type = row.get("Type", "").strip().capitalize()
        amount_str = row.get("Amount", "0").strip()
        desc = row.get("Description", "").strip()
        timestamp = row.get("Timestamp", "").strip()

        # Validate required fields
        if not username or not tx_type:
            return

        # Parse and validate amount
        amount = self._parse_amount(amount_str)
        if amount is None:
            print(f"Skipping invalid amount for {username}: {amount_str}")
            return

        # Process the transaction
        self._create_transaction(username, tx_type, amount, desc, timestamp)

    def _parse_amount(self, amount_str: str) -> Optional[float]:
        """Parse amount string to float with error handling."""
        try:
            return float(amount_str)
        except ValueError:
            return None

    def _create_transaction(self, username: str, tx_type: str, amount: float, 
                          description: str, timestamp: str):
        """Create a transaction for a user."""
        account_id = self._get_or_create_account(username)
        if not account_id:
            return

        cursor = self.db_conn.cursor()
        
        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, timestamp, description)
            VALUES (?, ?, ?, ?, ?)
        """, (account_id, tx_type, amount, timestamp, description))

        # Update account balance
        self._update_balance_from_transaction(account_id, tx_type, amount)

    def _get_or_create_account(self, username: str) -> Optional[int]:
        """Get existing account ID or create a new one."""
        account_id = self.get_account_id_by_username(username)
        if not account_id:
            success = self.create_account(username, "default123", 0, is_initial_load=True)
            if success is True:
                account_id = self.get_account_id_by_username(username)
        return account_id

    def _update_balance_from_transaction(self, account_id: int, tx_type: str, amount: float):
        """Update account balance based on transaction type."""
        cursor = self.db_conn.cursor()
        if tx_type.lower() == "deposit":
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", 
                         (amount, account_id))
        elif tx_type.lower() == "withdraw":
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", 
                         (amount, account_id))

    # ==================== AUTHENTICATION METHODS ====================
    
    def check_admin_credentials(self, username: str, password: str) -> bool:
        """Verify admin credentials."""
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT id FROM admins WHERE username=? AND password=?", 
            (username, password)
        )
        return cursor.fetchone() is not None

    def check_credentials(self, username: str, password: str) -> Optional[Tuple[int, str]]:
        """Verify user credentials and return user ID and username if valid."""
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT id, username FROM accounts WHERE username=? AND password=?", 
            (username, password)
        )
        return cursor.fetchone()

    # ==================== ACCOUNT MANAGEMENT ====================
    
    def create_account(self, username: str, password: str, initial_deposit: Union[str, float], 
                      is_initial_load: bool = False) -> Union[bool, str]:
        """
        Create a new user account with initial deposit.
        Returns True on success, error message on failure.
        """
        if not is_initial_load:
            validation_result = self._validate_initial_deposit(initial_deposit)
            if validation_result is not True:
                return validation_result
            initial_deposit = float(initial_deposit)

        cursor = self.db_conn.cursor()
        
        try:
            # Create account
            cursor.execute(
                "INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)", 
                (username, password, initial_deposit)
            )
            
            # Record initial deposit transaction
            new_account_id = cursor.lastrowid
            if initial_deposit > 0:
                self.record_transaction(
                    new_account_id, 'Deposit', initial_deposit, 
                    "Initial deposit on account creation"
                )
            
            self.db_conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return "Username already exists."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def _validate_initial_deposit(self, deposit: str) -> Union[bool, str]:
        """Validate initial deposit amount."""
        try:
            amount = float(deposit)
            if amount < 0:
                return "Initial deposit cannot be negative."
            return True
        except ValueError:
            return "Initial deposit must be a valid number."

    def get_balance(self, user_id: int) -> float:
        """Get current balance for user."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id=?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0.00

    def get_account_id_by_username(self, username: str) -> Optional[int]:
        """Get account ID by username."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE username=?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    def update_balance(self, user_id: int, amount: float):
        """Update user balance (positive for deposit, negative for withdrawal)."""
        cursor = self.db_conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id=?", 
            (amount, user_id)
        )
        self.db_conn.commit()

    # ==================== TRANSACTION MANAGEMENT ====================
    
    def record_transaction(self, account_id: int, transaction_type: str, 
                         amount: float, description: str = ""):
        """Record a transaction in the history."""
        cursor = self.db_conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, timestamp, description) 
            VALUES (?, ?, ?, ?, ?)
        """, (account_id, transaction_type, amount, timestamp, description))
        self.db_conn.commit()

    def get_transaction_history(self, user_id: int) -> List[Tuple]:
        """Get transaction history for a specific user."""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT timestamp, type, amount, description FROM transactions 
            WHERE account_id=? ORDER BY timestamp DESC
        """, (user_id,))
        return cursor.fetchall()

    # ==================== ADMIN METHODS ====================
    
    def get_all_accounts_summary(self) -> List[Tuple]:
        """Get summary of all user accounts for admin dashboard."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, username, balance FROM accounts ORDER BY id ASC")
        return cursor.fetchall()
        
    def get_all_transactions(self) -> List[Tuple]:
        """Get all transaction records across all users."""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT 
                t.timestamp, 
                a.username, 
                t.type, 
                t.amount, 
                t.description 
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            ORDER BY t.timestamp DESC
        """)
        return cursor.fetchall()
        
    def export_all_transactions_to_csv(self) -> Optional[str]:
        """Export all transactions to CSV file. Returns filename on success."""
        data = self.get_all_transactions()
        if not data:
            return None
            
        try:
            with open(CSV_EXPORT_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Username", "Type", "Amount", "Description"])
                writer.writerows(data)
            return str(CSV_EXPORT_FILENAME)
        except IOError as e:
            raise IOError(f"Failed to write CSV file {CSV_EXPORT_FILENAME}: {e}")

    # ==================== CLEANUP ====================
    
    def close(self):
        """Close database connection."""
        if self.db_conn:
            self.db_conn.close()

    def __del__(self):
        """Ensure database connection is closed on destruction."""
        self.close()