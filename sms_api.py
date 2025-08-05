from twilio.rest import Client

# Place your credentials securely, ideally use environment variables
TWILIO_ACCOUNT_SID = "your_account_sid_here"
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_PHONE = "your_twilio_phone_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_number, message):
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=to_number
        )
        print(f"SMS sent to {to_number}: SID {msg.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS to {to_number}: {e}")
        return False
