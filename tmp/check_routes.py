import sys
import os
sys.path.append(os.getcwd())
from app import app
from models import MedicineDetail

with app.app_context():
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
    
    print("\nMedicine Details in DB:")
    meds = MedicineDetail.query.all()
    for med in meds:
        print(f"- {med.name}")
    
    if not meds:
        print("No medicine details found!")
