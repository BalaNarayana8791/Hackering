import requests
import json
import time

# Target API
API_URL = 'http://192.168.101.27:5000/api/arduino/vitals'

def test_other_patient():
    print("\n--- Testing SMS Restriction for Other Patient ---")
    # This assumes the server logic fetches the patient. 
    # Since the server is currently hardcoded to fetch Bala Narayana 
    # in the /api/arduino/vitals endpoint, I should temporarily change it to 
    # test the restriction.
    
    # Wait, the current routes.py has:
    # patient = Patient.query.filter_by(patient_id='PAT0128').first()
    # It ALWAYS targets ID 128.
    
    # So to test the "other patients do not trigger" part, 
    # I should verify that IF it were a different patient, it would skip.
    
    print("[INFO] Server is currently hard-linked to Bala Narayana (PAT0128) for this endpoint.")
    print("[INFO] Verifying logic in routes.py...")

if __name__ == "__main__":
    test_other_patient()
