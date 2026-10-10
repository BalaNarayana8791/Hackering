import requests
import sys

def test_medicine_api(med_name):
    url = f"http://localhost:5000/api/medicine-details/{med_name}"
    try:
        response = requests.get(url)
        print(f"Testing API for {med_name}...")
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
    # Test for Paracetamol as requested by user
    success = test_medicine_api("Paracetamol")
    if success:
        print("\nSUCCESS: Medicine details API is working correctly.")
    else:
        print("\nFAILURE: Medicine details API test failed.")
        sys.exit(1)
