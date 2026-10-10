import os
import sys

sys.path.append(os.getcwd())

from app import app, db
from models import Patient, StaffMember

with app.app_context():
    p = Patient.query.get(128)
    if p:
        print(f"Patient ID: {p.id}, Name: {p.full_name}, Room: {p.room_number}")
        doc = StaffMember.query.get(p.assigned_doctor_id) if p.assigned_doctor_id else None
        nrs = StaffMember.query.get(p.assigned_nurse_id) if p.assigned_nurse_id else None
        print(f"  Assigned Doctor: {doc.staff_id if doc else 'None'}")
        print(f"  Assigned Nurse: {nrs.staff_id if nrs else 'None'}")
    else:
        print("Patient ID 128 not found.")
