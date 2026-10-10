import requests
import json
import time

# Try both localhost and the local network IP
API_URLS = [
    'http://127.0.0.1:5000/api/arduino/vitals',
    'http://192.168.1.4:5000/api/arduino/vitals'
]

print("--- Med-Alert Diagnostic: Manual Vital Push ---")
print("Targeting: Bala Narayana (PAT0128)")

# Standard test values
payload = {
    'bpm': 75,
    'spo2': 98,
    'temp': 98.6
}

success = False
for url in API_URLS:
    try:
        print(f"Trying to push test data to {url}...")
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            print(f"\n[OK] SUCCESSFULLY pushed test vitals to {url}!")
            print("--- Verification Check ---")
            print("1. Go to your Doctor Dashboard tab.")
            print("2. Look at the card for PAT0128.")
            print("3. Vitals should now show BPM: 75, SpO2: 98, Temp: 98.6.")
            print("---------------------------")
            success = True
            break
        else:
            print(f"Server at {url} returned error code {response.status_code}")
    except Exception as e:
        print(f"Could not reach {url}: {e}")

if not success:
    print("\n[FAILED]: Could not reach any server endpoint.")
    print("TIP: Is your Med-Alert application running?")
