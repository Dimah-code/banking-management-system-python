import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = DATA_DIR / "exports"
DATABASES_DIR = DATA_DIR / "databases"

# Ensure directories exist
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATABASES_DIR.mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PATH = DATABASES_DIR / DATABASE_NAME

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# File paths
CSV_EXPORT_FILENAME = EXPORTS_DIR / "system_transactions.csv"
INITIAL_ACCOUNTS_FILE = EXPORTS_DIR / "system_transactions.csv"

# Application settings
APP_NAME = "Banking Management System"
APP_VERSION = "1.0.0"