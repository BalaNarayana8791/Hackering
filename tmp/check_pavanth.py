import os
import sys

# Add the current directory to the search path for imports
sys.path.append(os.getcwd())

from app import app, db
from models import Patient, VitalSign

with app.app_context():
    patients = Patient.query.filter((Patient.first_name + ' ' + Patient.last_name).ilike('%bala narayana%')).all()
    print(f"Found {len(patients)} matching patients:")
    for p in patients:
        print(f"ID: {p.id}, PatientID: {p.patient_id}, Name: {p.full_name}, Room: {p.room_number}")
        vitals_count = VitalSign.query.filter_by(patient_id=p.id).count()
        print(f"  Vitals Count: {vitals_count}")
        if vitals_count > 0:
            latest = VitalSign.query.filter_by(patient_id=p.id).order_by(VitalSign.recorded_at.desc()).first()
            print(f"  Latest: BPM:{latest.heart_rate}, SPO2:{latest.oxygen_saturation}, Temp:{latest.temperature} at {latest.recorded_at}")
