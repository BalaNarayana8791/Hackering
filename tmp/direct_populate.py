import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import MedicineDetail
from synthetic_data import populate_medicine_details

with app.app_context():
    print("Populating medicine details...")
    populate_medicine_details()
    print("Done.")
    
    meds = MedicineDetail.query.all()
    print(f"Total medicines in DB: {len(meds)}")
    for med in meds:
        print(f"- {med.name}: {med.usage[:50]}...")
