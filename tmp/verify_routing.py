import sys
import os
sys.path.append(os.getcwd())

from app import app, db
from models import Patient, AppointmentRequest, StaffMember
from appointment_routing import appointment_router, notification_service
from datetime import datetime, timedelta

with app.app_context():
    # Find a patient
    patient = Patient.query.first()
    if not patient:
        patient = Patient(patient_id="TEST001", first_name="Test", last_name="Patient", date_of_birth=datetime(1990,1,1).date(), gender="male")
        db.session.add(patient)
        db.session.commit()
    
    # Create an appointment request
    appt = AppointmentRequest(
        patient_id=patient.id,
        department="General Medicine",
        preferred_date=datetime.now() + timedelta(days=1),
        preferred_time="09:00",
        notes="Final verification of fixed method name",
        urgency="normal"
    )
    db.session.add(appt)
    db.session.commit()
    print(f"Created appt {appt.id}")
    
    print("Initiating routing (calling route_appointment)...")
    doctor = appointment_router.route_appointment(appt)
    
    if doctor:
        print(f"Allocated to Dr. {doctor.first_name}")
        notification_service.send_appointment_confirmation(appt, doctor)
        print("Success! Method route_appointment found and executed.")
    else:
        print("Routing failed.")
