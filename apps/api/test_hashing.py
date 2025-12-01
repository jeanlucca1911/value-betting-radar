from core.security import get_password_hash, verify_password

try:
    pwd = "password123"
    print(f"Hashing '{pwd}'...")
    hashed = get_password_hash(pwd)
    print(f"[OK] Hash: {hashed}")
    
    print("Verifying...")
    is_valid = verify_password(pwd, hashed)
    print(f"[OK] Valid: {is_valid}")
except Exception as e:
    print(f"[FAIL] Error: {e}")
