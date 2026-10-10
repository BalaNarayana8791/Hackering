import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

print(f"Connecting to Twilio account: {account_sid}...")
try:
    client = Client(account_sid, auth_token)
    incoming_phone_numbers = client.incoming_phone_numbers.list(limit=10)
    
    if not incoming_phone_numbers:
        print("No incoming phone numbers found for this account.")
    else:
        for record in incoming_phone_numbers:
            print(f"Found Twilio Phone Number: {record.phone_number} ({record.friendly_name})")
except Exception as e:
    print(f"Error listing phone numbers: {e}")
