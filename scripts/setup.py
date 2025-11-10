#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def setup_environment():
    env_example = Path("example.env")
    env_file = Path(".env")
    
    if not env_file.exists():
        shutil.copy(env_example, env_file)
        print("Created .env file from example. Please edit it with your settings.")
    else:
        print(".env file already exists.")
    
    # Create necessary directories
    Path("data/exports").mkdir(parents=True, exist_ok=True)
    Path("data/backups").mkdir(parents=True, exist_ok=True)
    Path("data/databases").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    setup_environment()