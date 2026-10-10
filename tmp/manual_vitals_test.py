import requests
import json
import time

url = 'http://127.0.0.1:5000/api/arduino/vitals'
payload = {
    'bpm': 75,
    'spo2': 98,
    'temp': 98.6
}

print(f"Sending POST to {url}...")
try:
    response = requests.post(url, json=payload, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
