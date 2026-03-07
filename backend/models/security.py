import secrets
import uuid
import time
from datetime import datetime
from cryptography.fernet import Fernet

#0. Generate a secret id
def generate_secret_key():
    key_byte =  Fernet.generate_key()
    key_str = key_byte.decode("utf-8")
    return [key_byte, key_str]
# 1. GENERATOR: Creates a long, non-repeating key
def generate_unique_key():
    """Generates a long key with random bits and a high-precision time signature."""
    # High-precision time signature (Hex)
    timestamp_hex = hex(int(time.time_ns()))[2:] 
    
    # Human-readable date signature (Hex)
    date_sig = datetime.now().strftime("%Y%m%d%H%M%S").encode().hex()
    
    # Random components
    secure_rand = secrets.token_hex(32)
    unique_id = uuid.uuid4().hex
    
    # Combine components into a long key
    full_key = f"{timestamp_hex}-{date_sig}-{unique_id}-{secure_rand}"
    return full_key
def reversible_hasher(data, secret_key):
    """Encrypts the data safely, handling string or bytes input."""
    f = Fernet(secret_key)
    
    # Ensure data is bytes
    if isinstance(data, str):
        data_bytes = data.encode()
    elif isinstance(data, bytes):
        data_bytes = data
    else:
        # Fallback: convert to string, then bytes
        data_bytes = str(data).encode()
    
    # Encrypt and return string
    encrypted_bytes = f.encrypt(data_bytes)
    return encrypted_bytes.decode()

# 2. HASHER: Reversible 'hashing' (Encryption)
def reversible_dehasher(token, secret_key):
    """Decrypts the token safely, handling string or bytes input."""
    if not token:
        print("No token found")
        return None

    f = Fernet(secret_key)

    # Ensure token is bytes
    if isinstance(token, bytes):
        token_bytes = token
    else:
        token_bytes = str(token).encode()
    
    try:
        decrypted_bytes = f.decrypt(token_bytes)
        return decrypted_bytes.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def check_key(hashed_key, original_key, secret_key):
    if reversible_dehasher(hashed_key, secret_key) == original_key:
        return True
    else:
        return False
if __name__ == "__main__":    
    # --- EXAMPLE USAGE ---
    # Generate a master encryption key (must be kept safe to 'dehash' later)
    master_key = Fernet.generate_key() 

    # Step 1: Create the unique key
    original_key = generate_unique_key()
    print(f"Original Key:\n{original_key}\n")

    # Step 2: 'Hash' the key
    hashed_key = reversible_hasher(original_key, master_key)
    print(f"Hashed (Encrypted) Key:\n{hashed_key}\n")

    # Step 3: 'Dehash' the key
    dehashed_key = reversible_dehasher(hashed_key, master_key)
    print(f"Dehashed (Decrypted) Key:\n{dehashed_key}")

    # Verification
    assert original_key == dehashed_key, "Dehashed key does not match original!"
