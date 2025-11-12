#!/usr/bin/env python3
"""
Banking Management System - Main Entry Point
A secure banking application with user and admin interfaces.
"""

import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Main application entry point."""
    try:
        from gui.app import BankingApp
        print("🚀 Starting Banking Management System...")
        
        # Create and run the application
        app = BankingApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please make sure all dependencies are installed and paths are correct.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()