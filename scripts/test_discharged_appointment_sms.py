import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Patient, AppointmentRequest, StaffMember
from ai_appointment_router import notification_service

def setup_test_data():
    with app.app_context():
        # Create a test patient (discharged)
        patient_id = 'DISCH_TEST_001'
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if patient:
            # Cleanup
            AppointmentRequest.query.filter_by(patient_id=patient.id).delete()
            db.session.delete(patient)
            db.session.commit()
            
        patient = Patient(
            patient_id=patient_id,
            first_name='Discharged',
            last_name='Patient',
            date_of_birth=datetime(1985, 5, 20).date(),
            gender='Female',
            status='discharged',
            phone='9876543210'
        )
        db.session.add(patient)
        db.session.commit()
        return patient.id

def test_discharged_sms(patient_id):
    with app.app_context():
        # 1. Booking
        print("\n--- Testing DISCHARGED Booking SMS ---")
        appt = AppointmentRequest(
            patient_id=patient_id,
            preferred_date=datetime.now() + timedelta(days=2),
            preferred_time='11:30 AM',
            notes='Follow-up after discharge',
            status='pending',
            source='discharged_portal',
            appointment_type='follow-up',
            department='Cardiology'
        )
        db.session.add(appt)
        db.session.commit()
        
        notification_service.send_booking_notification(appt)
        
        # 2. Confirmation
        print("\n--- Testing DISCHARGED Confirmation SMS ---")
        doctor = StaffMember.query.filter_by(role='doctor').first()
        doctor_name = f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Dr. Smith"
        
        notification_service.send_appointment_confirmation(appt, doctor)

if __name__ == "__main__":
    # Force print in _send_sms for verification
    notification_service._send_sms = lambda ph, msg: print(f"[V-SMS] To: {ph} | Message: {msg}") or True
    
    try:
        p_id = setup_test_data()
        test_discharged_sms(p_id)
        print("\nDischarged patient verification complete.")
    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
