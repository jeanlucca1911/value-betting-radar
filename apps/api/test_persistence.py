import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_persistence():
    email = "persist_test@example.com"
    password = "testpass123"
    
    # 1. Register
    print("1. Registering new user...")
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if reg_res.status_code == 201:
        print(f"   [OK] User registered: {email}")
    elif "already registered" in reg_res.text:
        print(f"   [INFO] User already exists (persistence working!)")
    else:
        print(f"   [FAIL] Registration failed: {reg_res.text}")
        return
    
    # 2. Login
    print("2. Logging in...")
    login_res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
    if login_res.status_code == 200:
        token = login_res.json()["access_token"]
        print(f"   [OK] Login successful")
    else:
        print(f"   [FAIL] Login failed: {login_res.text}")
        return
    
    # 3. Place a bet
    print("3. Placing shadow bet...")
    bet_data = {
        "match_id": "test123",
        "home_team": "Team A",
        "away_team": "Team B",
        "selection": "Team A",
        "odds": 2.5,
        "stake": 100,
        "bookmaker": "Betfair",
        "edge": 5.2,
        "user_email": email
    }
    bet_res = requests.post(f"{BASE_URL}/bets/place", json=bet_data)
    if bet_res.status_code == 200:
        bet_id = bet_res.json()["bet_id"]
        print(f"   [OK] Bet placed with ID: {bet_id}")
    else:
        print(f"   [FAIL] Bet placement failed: {bet_res.text}")
        return
    
    # 4. Get bet history
    print("4. Fetching bet history...")
    history_res = requests.get(f"{BASE_URL}/bets/history?user_email={email}")
    if history_res.status_code == 200:
        history = history_res.json()
        print(f"   [OK] Found {history['total']} bets in history")
        if history['bets']:
            print(f"   Latest bet: {history['bets'][0]['selection']} @ {history['bets'][0]['odds']}")
    else:
        print(f"   [FAIL] History fetch failed: {history_res.text}")
    
    print("\n[SUCCESS] Persistence test complete!")
    print("Restart the backend and run this script again to verify data persists.")

if __name__ == "__main__":
    test_persistence()
