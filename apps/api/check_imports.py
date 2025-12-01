try:
    from jose import jwt
    print("[OK] jose imported")
except ImportError as e:
    print(f"[FAIL] jose import failed: {e}")

try:
    from passlib.context import CryptContext
    print("[OK] passlib imported")
except ImportError as e:
    print(f"[FAIL] passlib import failed: {e}")

try:
    import cryptography
    print("[OK] cryptography imported")
except ImportError as e:
    print(f"[FAIL] cryptography import failed: {e}")
