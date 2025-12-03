import requests
import json

BASE_URL = "https://value-betting-radar-production.up.railway.app/api/v1"

print("Testing registration on production...")
register_data = {
    "email": "test_prod_user@example.com",
    "password": "testpass123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
