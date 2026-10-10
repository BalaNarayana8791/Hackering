import sys
import os
from datetime import datetime, timedelta
import logging

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Patient, AppointmentRequest
from ai_appointment_router import notification_service

def test_phone_update():
    with app.app_context():
        print("\n--- Testing Patient Phone Update ---")
        
        # 1. Setup existing patient
        email = "phone_update_test@example.com"
        old_phone = "1111111111"
        new_phone = "9999999999"
        
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            # Clean up old appointments
            AppointmentRequest.query.filter_by(patient_id=patient.id).delete()
            patient.phone = old_phone
            db.session.commit()
        else:
            patient = Patient(
                patient_id='PAT_UPDATE_001',
                first_name='Phone',
                last_name='Tester',
                email=email,
                phone=old_phone,
                date_of_birth=datetime(1990, 1, 1).date(),
                gender='Male'
            )
            db.session.add(patient)
            db.session.commit()
            
        print(f"Initial patient phone: {patient.phone}")
        
        # 2. Simulate book_appointment_public logic for existing patient with NEW phone
        # Mirroring the logic I just added to routes.py
        patient_from_db = Patient.query.filter_by(email=email).first()
        if patient_from_db:
            if new_phone and patient_from_db.phone != new_phone:
                patient_from_db.phone = new_phone
                db.session.commit()
                print(f"Updated phone to: {patient_from_db.phone}")
        
        # 3. Verify SMS is sent to NEW phone
        appt = AppointmentRequest(
            patient_id=patient_from_db.id,
            preferred_date=datetime.now() + timedelta(days=1),
            status='pending'
        )
        db.session.add(appt)
        db.session.commit()
        
        print(f"Sending notification for appt {appt.id}...")
        
        sent_to = []
        notification_service._send_sms = lambda ph, msg: sent_to.append(ph) or True
        notification_service.send_booking_notification(appt)
        
        if new_phone in sent_to or f"+91{new_phone}" in sent_to:
            print(f"[SUCCESS] SMS sent to NEW phone number: {sent_to[0]}")
        else:
            print(f"[FAIL] SMS sent to wrong number: {sent_to[0] if sent_to else 'None'}")

if __name__ == "__main__":
    test_phone_update()
