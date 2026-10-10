import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Patient

with app.app_context():
    patients = Patient.query.all()
    for p in patients:
        if 'Bala' in p.full_name:
            print(f"ID: {p.id}, PatientID: {p.patient_id}, Name: {p.full_name}")
