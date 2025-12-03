import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Register a new user
print("Testing registration...")
register_data = {
    "email": "test@example.com",
    "password": "testpass123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Login
print("\nTesting login...")
login_data = {
    "username": "test@example.com",
    "password": "testpass123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    
    if response.status_code == 200:
        token = result.get("access_token")
        print(f"\n✅ Login successful! Token: {token[:20]}...")
except Exception as e:
    print(f"Error: {e}")
