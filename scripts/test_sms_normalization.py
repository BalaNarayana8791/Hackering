import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_appointment_router import AppointmentNotificationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_normalization():
    service = AppointmentNotificationService()
    
    test_cases = [
        ("8885494025", "+918885494025"),
        ("08885494025", "+918885494025"),
        ("+918885494025", "+918885494025"),
        ("918885494025", "+918885494025"),
        ("888 549 4025", "+918885494025"),
        ("888-549-4025", "+918885494025"),
        ("+13393297701", "+13393297701"), # US number test
    ]
    
    # Mock _send_sms_twilio and _send_sms_aws to capture normalized phone
    normalized_results = []
    service._send_sms_twilio = lambda ph, msg: normalized_results.append(ph) or True
    service._send_sms_aws = lambda ph, msg: normalized_results.append(ph) or True
    service.sms_provider = 'twilio' # Force twilio to capture result

    print("\n--- Testing Phone Number Normalization ---")
    all_passed = True
    for input_phone, expected in test_cases:
        normalized_results.clear()
        service._send_sms(input_phone, "Test message")
        actual = normalized_results[0] if normalized_results else "FAILED"
        
        status = "[OK]" if actual == expected else "[FAIL]"
        if actual != expected: all_passed = False
        print(f"{status} Input: {input_phone:15} | Expected: {expected:15} | Actual: {actual:15}")
    
    if all_passed:
        print("\nAll normalization tests passed!")
    else:
        print("\nSome normalization tests failed.")

if __name__ == "__main__":
    test_normalization()
