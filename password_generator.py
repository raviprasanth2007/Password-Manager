import string
import random

def generate_strong_password(length=16):
    """Generates a highly secure password containing upper, lower, numbers, and symbols."""
    if length < 8:
        length = 8
        
    # Ensure at least one character of each type is included
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    symbol = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
    
    # Fill the rest with random choices from the combined pool
    pool = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    remaining = [random.choice(pool) for _ in range(length - 4)]
    
    # Combine and shuffle
    pwd_chars = [upper, lower, digit, symbol] + remaining
    random.shuffle(pwd_chars)
    
    return ''.join(pwd_chars)
