import os
import sys
sys.path.append(os.getcwd())
try:
    from app import app, db
except ImportError:
    # If standard import fails, try relative or adjust path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    from app import app, db
from models import StaffMember, Patient, Alert

def check_db():
    with app.app_context():
        # Find DOC_RT and NRS_RT
        doc_rt = StaffMember.query.filter_by(staff_id="DOC_RT").first()
        nrs_rt = StaffMember.query.filter_by(staff_id="NRS_RT").first()

        if not doc_rt:
            print("DOC_RT not found")
        else:
            print(f"DOC_RT: {doc_rt.full_name} (ID: {doc_rt.id})")
            patients = Patient.query.filter_by(assigned_doctor_id=doc_rt.id).all()
            print(f"  Assigned patients: {[p.full_name for p in patients]}")

        if not nrs_rt:
            print("NRS_RT not found")
        else:
            print(f"NRS_RT: {nrs_rt.full_name} (ID: {nrs_rt.id})")
            patients = Patient.query.filter_by(assigned_nurse_id=nrs_rt.id).all()
            print(f"  Assigned patients: {[p.full_name for p in patients]}")

        # Check for any other patients in the system
        all_patients = Patient.query.all()
        print(f"Total patients in system: {len(all_patients)}")
        for p in all_patients:
            if p.assigned_doctor_id not in [doc_rt.id if doc_rt else None] and p.assigned_nurse_id not in [nrs_rt.id if nrs_rt else None]:
                # print(f"  Found other patient: {p.full_name} (ID: {p.patient_id}) - Doctor ID: {p.assigned_doctor_id}, Nurse ID: {p.assigned_nurse_id}")
                pass

if __name__ == "__main__":
    check_db()
