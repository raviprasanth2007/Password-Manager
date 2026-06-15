from cryptography.fernet import Fernet
import os

KEY_FILE = 'encryption_key.txt'

def _get_key():
    """Reads the secure key from file or generates one if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key
    else:
        with open(KEY_FILE, 'rb') as f:
            return f.read().strip()

# Initialize Fernet globally with the key
cipher = Fernet(_get_key())

def encrypt_password(plain_text):
    """Takes a plain string and returns an encrypted byte string."""
    return cipher.encrypt(plain_text.encode('utf-8'))

def decrypt_password(encrypted_data):
    """Takes encrypted bytes and returns the original plain string."""
    try:
        if isinstance(encrypted_data, str):
            # If the database returned a string instead of bytes, encode it back
            encrypted_data = encrypted_data.encode('utf-8')
        return cipher.decrypt(encrypted_data).decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return "DECRYPTION_FAILED"
