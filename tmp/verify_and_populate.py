import requests
import sys
import time

def trigger_init_data():
    url = "http://localhost:5000/init-data"
    try:
        print("Triggering /init-data to populate medicine details...")
        response = requests.get(url, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        # Even if it redirects to index, it should have executed the initialization
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def test_medicine_api(med_name):
    url = f"http://localhost:5000/api/medicine-details/{med_name}"
    try:
        response = requests.get(url)
        print(f"\nTesting API for {med_name}...")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response Data:")
            print(f"  Name: {data.get('name')}")
            print(f"  Usage: {data.get('usage')}")
            print(f"  Dosage: {data.get('dosage')}")
            print(f"  Precautions: {data.get('precautions')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    if trigger_init_data():
        # Wait a bit for DB to commit if needed
        time.sleep(2)
        
        # Test for Paracetamol
        success = test_medicine_api("Paracetamol")
        if success:
            print("\nSUCCESS: Medicine details API is working correctly after initialization.")
        else:
            print("\nFAILURE: Medicine details API test failed even after initialization.")
            sys.exit(1)
    else:
        print("\nFAILURE: Could not trigger /init-data.")
        sys.exit(1)
