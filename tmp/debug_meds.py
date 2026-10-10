from app import app, db
from models import Patient, Medication
import json

def verify_meds():
    with app.app_context():
        p6 = Patient.query.filter_by(patient_id='PAT000006').first()
        if not p6:
            print("P6 not found")
            return
            
        meds = Medication.query.filter_by(patient_id=p6.id).all()
        print(f"Medications for {p6.full_name} ({p6.patient_id}):")
        for m in meds:
            print(f"ID: {m.id}, Name: '{m.name}', Dosage: {m.dosage}, Start: {m.start_date}, Route: {m.route}")

if __name__ == "__main__":
    verify_meds()
