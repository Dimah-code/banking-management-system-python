"""
Input validators for the banking system.
"""

def validate_amount(amount_str):
    """
    Validate amount input and return float value.
    Returns (success, value_or_error_message)
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be positive."
        return True, amount
    except ValueError:
        return False, "Please enter a valid number."


def validate_username(username):
    """
    Validate username format.
    Returns (success, message)
    """
    if not username or not username.strip():
        return False, "Username is required."
    
    username = username.strip()
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    
    if len(username) > 20:
        return False, "Username must be less than 20 characters."
    
    if not username.replace('_', '').isalnum():
        return False, "Username can only contain letters, numbers, and underscores."
    
    return True, username