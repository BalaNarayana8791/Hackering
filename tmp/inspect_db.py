import sys
import os
sys.path.append(os.getcwd())

from app import app, db
from models import StaffMember

with app.app_context():
    staff = StaffMember.query.filter_by(role='doctor').limit(10).all()
    print("Sample Doctors:")
    for s in staff:
        print(f"ID: {s.staff_id}, Name: {s.first_name} {s.last_name}, Role: {s.role}, Dept: {s.department}, Spec: {s.specialization}")
    
    unique_specs = db.session.query(StaffMember.specialization).distinct().all()
    print(f"Unique Specializations: {[s[0] for s in unique_specs]}")
    unique_depts = db.session.query(StaffMember.department).distinct().all()
    print(f"Unique Departments: {[d[0] for d in unique_depts]}")
