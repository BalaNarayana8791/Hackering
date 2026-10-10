import sys
import os
import logging
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Patient, AppointmentRequest, StaffMember
from ai_appointment_router import notification_service

def setup_test_data():
    with app.app_context():
        # Create a test patient
        patient = Patient.query.filter_by(patient_id='SMS_TEST_001').first()
        if patient:
            # Cleanup
            AppointmentRequest.query.filter_by(patient_id=patient.id).delete()
            db.session.delete(patient)
            db.session.commit()
            
        patient = Patient(
            patient_id='SMS_TEST_001',
            first_name='SMS',
            last_name='Tester',
            date_of_birth=datetime(1990, 1, 1).date(),
            gender='Male',
            phone='1234567890'
        )
        db.session.add(patient)
        db.session.commit()
        return patient.id

def test_sms_booking(patient_id):
    print("\n--- Testing Booking SMS ---")
    with app.app_context():
        # Create appointment request
        appt = AppointmentRequest(
            patient_id=patient_id,
            preferred_date=datetime.now() + timedelta(days=1),
            preferred_time='10:00 AM',
            notes='Test booking',
            status='pending',
            source='patient_portal'
        )
        db.session.add(appt)
        db.session.commit()
        
        print(f"Simulating booking notification for appointment {appt.id}...")
        # This will trigger the _send_sms (mock) which logs to logger.info
        success = notification_service.send_booking_notification(appt)
        
        if success:
            print("[OK] send_booking_notification returned True")
        else:
            print("[FAIL] send_booking_notification returned False")

def test_sms_confirmation(patient_id):
    print("\n--- Testing Confirmation SMS ---")
    with app.app_context():
        # Get/create appointment
        appt = AppointmentRequest.query.filter_by(patient_id=patient_id).first()
        
        # Confirmation wording test
        print(f"Simulating confirmation notification for appointment {appt.id}...")
        success = notification_service.send_appointment_confirmation(appt)
        
        if success:
            print("[OK] send_appointment_confirmation returned True")
        else:
            print("[FAIL] send_appointment_confirmation returned False")

if __name__ == "__main__":
    # Force print in _send_sms for verification
    notification_service._send_sms = lambda ph, msg: print(f"[V-SMS] To: {ph} | Message: {msg}") or True
    
    try:
        p_id = setup_test_data()
        test_sms_booking(p_id)
        test_sms_confirmation(p_id)
        print("\nVerification complete. Check the logs above for '[MOCK SMS]' segments.")
    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
