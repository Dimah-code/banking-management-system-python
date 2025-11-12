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
DATABASE_NAME = os.getenv("DATABASE_NAME", "banking_data.db")  # ✅ اول تعریف کن
DATABASE_PATH = DATABASES_DIR / DATABASE_NAME

# حالا می‌تونی چاپ کنی
print(f"DATABASES_DIR: {DATABASES_DIR}")
print(f"DATABASE_NAME: {DATABASE_NAME}")
print(f"Type of DATABASE_NAME: {type(DATABASE_NAME)}")

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# File paths
CSV_EXPORT_FILENAME = EXPORTS_DIR / "system_transactions.csv"
INITIAL_ACCOUNTS_FILE = EXPORTS_DIR / "system_transactions.csv"  # این هم احتمالاً باید متفاوت باشد


# Theme

BG_DARK = "#1a1a2e"         # Deep Navy Blue Background (Container)
BG_PRIMARY = "#16213e"      # Richer blue for main content
FG_LIGHT = "#eeeeee"        # Lighter text for better contrast
ACCENT_BLUE = "#0f3460"     # Deep Royal Blue accent
SIDEBAR_COLOR = "#0d0d1a"   # Very dark navy for the sidebar
SUCCESS_GREEN = "#4ade80"   # Modern vibrant green
WARNING_RED = "#f87171"     # Soft red for warnings
ADMIN_COLOR = "#fbbf24"     # Amber gold for admin

# Fonts
FONT_STYLE = ("Inter", 12)
HEADER_FONT_STYLE = ("Inter", 16, "bold")
TITLE_FONT_STYLE = ("Inter", 28, "bold")
BUTTON_FONT_STYLE = ("Inter", 14, "bold")


# Application settings
APP_NAME = "Banking Management System"
APP_VERSION = "1.0.0"