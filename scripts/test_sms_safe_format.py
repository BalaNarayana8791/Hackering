import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_number = os.environ.get('TWILIO_PHONE_NUMBER')
to_number = "+917675996314"

client = Client(account_sid, auth_token)

# 6. "Safe" version: Includes brand but is more concise
safe_body = (
    "Dear User,\n"
    "Your appointment is booked at Narayana Hospital.\n\n"
    "No: APT9999\n"
    "Dept: Cardiology\n"
    "Date: 25-03-2026\n"
    "Time: 10:30 AM\n\n"
    "Pls arrive 10m early. For help call 9999888877. Good health!"
)

try:
    message = client.messages.create(
        body=safe_body,
        from_=from_number,
        to=to_number
    )
    print(f"Safe Format Test SID: {message.sid}, Status: {message.status}")
except Exception as e:
    print(f"Error: {e}")
