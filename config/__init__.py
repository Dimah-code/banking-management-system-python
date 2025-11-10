import os
from .settings import *

# Determine environment
environment = os.getenv("APP_ENV", "development")

if environment == "production":
    from .production import *
elif environment == "development":
    from .development import *