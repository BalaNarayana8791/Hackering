
import sys
import os
sys.path.append(os.getcwd())

from app import app, db
from models import Patient, AppointmentRequest
from datetime import datetime

def test_discharged_booking():
    with app.app_context():
        # Find a discharged patient
        patient = Patient.query.filter_by(status='discharged').first()
        if not patient:
            print("No discharged patient found for testing.")
            return

        print(f"Testing with Patient: {patient.full_name} ({patient.patient_id})")
        
        # Simulate the API call
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['patient_id'] = patient.id
            
            payload = {
                "preferred_date": datetime.now().strftime("%Y-%m-%d"),
                "preferred_time": "11:30 AM",
                "notes": "Follow-up checkup after discharge",
                "department": "Cardiology"
            }
            
            print(f"Sending booking request: {payload}")
            response = client.post('/api/discharged/book-appointment', 
                                   json=payload,
                                   follow_redirects=True)
            
            print(f"Status Code: {response.status_code}")
            data = response.get_json()
            print(f"Response Data: {data}")
            
            if response.status_code == 200 and data.get('ok'):
                appt_id = data.get('appointment_id')
                appt = AppointmentRequest.query.get(appt_id)
                if appt:
                    print(f"SUCCESS: Appointment {appt_id} created in database.")
                else:
                    print("FAILURE: Appointment not found in database.")
            
            # Test Dashboard Rendering
            print("\nTesting Dashboard Rendering...")
            dash_resp = client.get('/patient-portal/dashboard')
            print(f"Dashboard Status Code: {dash_resp.status_code}")
            if b'Med-Alert Assistant - Chat' in dash_resp.data:
                print("SUCCESS: Rendered specialized discharged dashboard.")
            else:
                print("FAILURE: Did not render specialized discharged dashboard.")
                
            # Test Summary API
            print("\nTesting Summary API...")
            sum_resp = client.get('/api/discharged/summary')
            print(f"Summary Status Code: {sum_resp.status_code}")
            if sum_resp.status_code == 200:
                print(f"Summary Data: {sum_resp.get_json().keys()}")
                print("SUCCESS: Summary API functional.")
            else:
                print("FAILURE: Summary API failed.")

            # Test Clear History API
            print("\nTesting Clear History API...")
            clear_resp = client.post('/api/discharged/clear-history')
            print(f"Clear History Status Code: {clear_resp.status_code}")
            if clear_resp.status_code == 200:
                print("SUCCESS: Clear History API functional.")
            else:
                print("FAILURE: Clear History API failed.")

if __name__ == "__main__":
    test_discharged_booking()
