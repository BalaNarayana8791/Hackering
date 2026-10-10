import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Patient, VitalSign

with app.app_context():
    patient = Patient.query.filter_by(patient_id='PAT0128').first()
    if not patient:
        print("Patient PAT0128 not found!")
    else:
        print(f"Patient: {patient.full_name}")
        latest = VitalSign.query.filter_by(patient_id=patient.id).order_by(VitalSign.recorded_at.desc()).first()
        if latest:
            print(f"Latest Vital: BPM {latest.heart_rate}, SPO2 {latest.oxygen_saturation}, TEMP {latest.temperature}, STATUS {latest.status}, TIME {latest.recorded_at}")
        else:
            print("No vitals found for this patient.")
