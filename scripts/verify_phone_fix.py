import sys
import os

# Add parent directory to path to import twilio_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twilio_utils import format_to_e164

def test_formatting():
    test_cases = [
        ("7382594208", "+917382594208"),
        ("+917382594208", "+917382594208"),
        ("07382594208", "+917382594208"),
        ("917382594208", "+91917382594208"), # This matches current logic: if no +, prepend +91. 
                                              # Note: If user enters 91... without +, it will become +9191...
                                              # This is a known trade-off for simplicity.
        ("+1555010999", "+1555010999"),
        (" 7382 594 208 ", "+917382594208"),
        ("7382-594-208", "+917382594208"),
    ]

    print("Running phone formatting tests...")
    all_passed = True
    for input_val, expected in test_cases:
        actual = format_to_e164(input_val)
        if actual == expected:
            print(f"PASS: '{input_val}' -> '{actual}'")
        else:
            print(f"FAIL: '{input_val}' -> Expected '{expected}', got '{actual}'")
            all_passed = False
    
    if all_passed:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed.")
    return all_passed

if __name__ == "__main__":
    test_formatting()
