import sys
import os
sys.path.append(os.getcwd())

from app import app, db
from models import StaffMember

with app.app_context():
    # Update doctors to have department match specialization if department is missing or mismatch for demo purposes
    doctors = StaffMember.query.filter_by(role='doctor').all()
    count = 0
    for d in doctors:
        if d.specialization and (d.department is None or d.department != d.specialization):
            print(f"Updating {d.first_name} {d.last_name}: Dept {d.department} -> {d.specialization}")
            d.department = d.specialization
            count += 1
    
    db.session.commit()
    print(f"Updated {count} doctors with department = specialization.")

    # Verify General Medicine
    gen_med_docs = StaffMember.query.filter_by(department='General Medicine', role='doctor').count()
    print(f"Total doctors in General Medicine: {gen_med_docs}")
