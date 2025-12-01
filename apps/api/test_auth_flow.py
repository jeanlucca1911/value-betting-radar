import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_auth_flow():
    # 1. Register
    email = "test@example.com"
    password = "password123"
    
    print(f"Registering {email}...")
    try:
        reg_res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        if reg_res.status_code == 201:
            print("[OK] Registration successful")
        elif reg_res.status_code == 400 and "already registered" in reg_res.text:
            print("[WARN] User already registered (expected if re-running)")
        else:
            print(f"[FAIL] Registration failed: {reg_res.text}")
            return

        # 2. Login
        print("Logging in...")
        login_res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
        if login_res.status_code == 200:
            token = login_res.json()["access_token"]
            print(f"[OK] Login successful. Token: {token[:10]}...")
            
            # 3. Verify Protected Route
            print("Accessing protected route...")
            me_res = requests.get(f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {token}"})
            if me_res.status_code == 200:
                print("[OK] Protected route accessible")
            else:
                print(f"[FAIL] Protected route failed: {me_res.text}")
        else:
            print(f"[FAIL] Login failed: {login_res.text}")

    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    test_auth_flow()
