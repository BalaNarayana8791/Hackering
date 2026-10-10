from app import app, db
from models import Patient, Medication, AppointmentRequest
from datetime import datetime

def verify_setup():
    with app.app_context():
        # Check PAT000001 (Emergency) and PAT000006 (Discharged)
        p1 = Patient.query.filter_by(patient_id='PAT000001').first()
        p6 = Patient.query.filter_by(patient_id='PAT000006').first()
        
        print(f"PAT000001: {p1.full_name}, Status: {p1.status}")
        print(f"PAT000006: {p6.full_name}, Status: {p6.status}")
        
        # Check medications for p1 or p6
        meds = Medication.query.filter_by(patient_id=p6.id).all()
        print(f"Medications for {p6.full_name}:")
        for m in meds:
            print(f"- {m.name} ({m.dosage}, {m.frequency})")
            
        # Check if any appointments have been booked via the new route or recently
        appts = AppointmentRequest.query.filter_by(patient_id=p6.id).all()
        print(f"Appointments for {p6.full_name}: {len(appts)}")

if __name__ == "__main__":
    verify_setup()
