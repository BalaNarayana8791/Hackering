import os
from dotenv import load_dotenv
from twilio.rest import Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def test_twilio():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')
    to_number = "+917675996314" # Using a placeholder, I'll ask the user for their number if needed, or just see if the API call succeeds.

    if not all([account_sid, auth_token, from_number]):
        print("Missing Twilio credentials in .env")
        return

    try:
        client = Client(account_sid, auth_token)
        # Try to fetch account info first to verify credentials
        account = client.api.accounts(account_sid).fetch()
        print(f"Twilio Account Verified: {account.friendly_name}")
        
        # We won't actually send an SMS yet to avoid wasting credits, 
        # but verifying credentials is a good start.
        # Actually, let's try to send to a test number if possible, or just check if the client connects.
        
    except Exception as e:
        print(f"Twilio Error: {e}")

if __name__ == "__main__":
    test_twilio()
