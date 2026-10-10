import sys
import os
import time
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Patient, StaffMember, VitalSign, Alert, AlertRerouting
from vital_simulator import update_patient_vitals

def setup_test_data():
    """Setup a patient and staff for testing rerouting"""
    with app.app_context():
        # Find or create on-duty staff
        doc1 = StaffMember.query.filter_by(role='doctor', is_on_duty=True).first()
        nurse1 = StaffMember.query.filter_by(role='nurse', is_on_duty=True).first()
        
        doc2 = StaffMember.query.filter_by(role='doctor', is_on_duty=True).filter(StaffMember.id != (doc1.id if doc1 else 0)).first()
        nurse2 = StaffMember.query.filter_by(role='nurse', is_on_duty=True).filter(StaffMember.id != (nurse1.id if nurse1 else 0)).first()
        
        if not doc1 or not nurse1 or not doc2 or not nurse2:
            print("Error: Need at least 2 on-duty doctors and 2 on-duty nurses for this test.")
            return None, None, None
            
        # Create a test patient
        patient = Patient.query.filter_by(patient_id='TEST001').first()
        if patient:
            # Delete related records first
            Alert.query.filter_by(patient_id=patient.id).delete()
            AlertRerouting.query.filter_by(patient_id=patient.id).delete()
            VitalSign.query.filter_by(patient_id=patient.id).delete()
            db.session.delete(patient)
            db.session.commit()
            
        patient = Patient(
            patient_id='TEST001',
            first_name='Test',
            last_name='Patient',
            date_of_birth=datetime(1990, 1, 1).date(),
            gender='Other',
            status='emergency',
            assigned_doctor_id=doc1.id,
            assigned_nurse_id=nurse1.id,
            room_number='T1',
            bed_number='1'
        )
        db.session.add(patient)
        db.session.commit()
        
        print(f"Setup Patient: {patient.full_name}")
        print(f"Initial Doctor: {doc1.full_name}, Nurse: {nurse1.full_name}")
        print(f"Standby Doctor: {doc2.full_name}, Nurse: {nurse2.full_name}")
        
        return patient.id, (doc1.id, nurse1.id), (doc2.id, nurse2.id)

def simulate_critical_vitals(patient_id):
    """Simulate a critical vital sign for a patient to trigger an alert"""
    with app.app_context():
        from synthetic_data import generate_vital_sign, check_vital_thresholds
        from models import Alert
        
        patient = Patient.query.get(patient_id)
        # Force critical status
        vital = generate_vital_sign(patient, status_bias='critical')
        db.session.add(vital)
        db.session.commit()
        
        alert_data = check_vital_thresholds(vital)
        alert_ids = []
        for alert in alert_data:
            alert_obj = Alert(
                patient_id=patient.id,
                vital_sign_id=vital.id,
                alert_type=alert['type'],
                severity=alert['severity'],
                title=alert['title'],
                message=alert['message']
            )
            db.session.add(alert_obj)
            db.session.commit()
            alert_ids.append(alert_obj.id)
            
        print(f"  Generated {len(alert_data)} alerts (Critical: {any(a['severity']=='critical' for a in alert_data)})")
        return alert_ids

def run_test():
    patient_id, initial_staff, standby_staff = setup_test_data()
    if not patient_id:
        return

    # Trigger rerouting via vital_simulator logic
    # We need to call a modified version of the simulation or simulate 3 cycles
    
    print("\nSimulating 3 consecutive critical alerts...")
    
    # We'll use the logic from update_patient_vitals but target our test patient
    with app.app_context():
        # Initialize the counter if not exists
        if not hasattr(update_patient_vitals, "consecutive_critical_count"):
            update_patient_vitals.consecutive_critical_count = {}
        
        # Reset counter for our test patient
        update_patient_vitals.consecutive_critical_count[patient_id] = 0
        
        from vital_simulator import reroute_patient
        
        for i in range(1, 3):
            print(f"Cycle {i}:")
            alert_ids = simulate_critical_vitals(patient_id)
            
            # Application logic from vital_simulator.py
            update_patient_vitals.consecutive_critical_count[patient_id] = update_patient_vitals.consecutive_critical_count.get(patient_id, 0) + 1
            
            if update_patient_vitals.consecutive_critical_count[patient_id] >= 2:
                print("  Threshold reached! Triggering reroute...")
                patient = Patient.query.get(patient_id)
                reroute_patient(patient, alert_ids)
                update_patient_vitals.consecutive_critical_count[patient_id] = 0

    # Verification
    with app.app_context():
        patient = Patient.query.get(patient_id)
        print("\nVerification:")
        print(f"Final Doctor ID: {patient.assigned_doctor_id}")
        print(f"Final Nurse ID: {patient.assigned_nurse_id}")
        
        reroute_logs = AlertRerouting.query.filter_by(patient_id=patient_id).all()
        print(f"Reroute Logs Found: {len(reroute_logs)}")
        
        if patient.assigned_doctor_id != initial_staff[0] or patient.assigned_nurse_id != initial_staff[1]:
            print("\n[SUCCESS] Patient has been rerouted to new staff!")
            if reroute_logs:
                log = reroute_logs[0]
                print(f"[SUCCESS] Reroute log created accurately.")
                print(f"   Old Doc: {log.old_doctor_id}, New Doc: {log.new_doctor_id}")
        else:
            print("\n[FAILURE] Patient was not rerouted.")

if __name__ == "__main__":
    run_test()
