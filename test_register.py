import requests
import json

url = "https://value-betting-radar-production.up.railway.app/api/v1/auth/register"
headers = {
    "Content-Type": "application/json",
    "Origin": "https://www.valuebettingradar.com"
}
data = {
    "email": "finaltest@example.com",
    "password": "testpass123"
}

print("Testing registration endpoint...")
try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
