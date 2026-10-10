from models import Patient, db
from app import app
import logging

# Set logging level to error to avoid clutter
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

with app.app_context():
    p1 = Patient.query.filter_by(patient_id='PAT000001').first()
    p6 = Patient.query.filter_by(patient_id='PAT000006').first()
    
    if p1:
        print(f"PAT000001 Status: {p1.status}")
    else:
        print("PAT000001 not found")
        
    if p6:
        print(f"PAT000006 Status: {p6.status}")
    else:
        print("PAT000006 not found")
