from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    balance: float
    created_at: datetime

@dataclass
class Transaction:
    id: int
    account_id: int
    type: str
    amount: float
    timestamp: datetime
    description: str

@dataclass
class Admin:
    id: int
    username: str