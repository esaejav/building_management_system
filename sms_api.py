from twilio.rest import Client
import os

# Place your credentials securely via environment variables in production
# Fallback to placeholders if not set
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid_here")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token_here")

# Twilio WhatsApp sender must be prefixed with 'whatsapp:'
# Example for sandbox: 'whatsapp:+14155238886'
# Or your approved WhatsApp-enabled number: 'whatsapp:+1XXXXXXXXXX'
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Optional: Twilio SMS number if you still want SMS support
TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM", "your_twilio_phone_number")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_number, message):
    """
    Send a plain SMS using Twilio (requires a Twilio SMS-capable number).
    to_number should be in E.164 format, e.g., +15551234567
    """
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_SMS_FROM,
            to=to_number
        )
        print(f"SMS sent to {to_number}: SID {msg.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS to {to_number}: {e}")
        return False


def send_whatsapp(to_number, message):
    """
    Send a WhatsApp message using Twilio's WhatsApp API.

    Parameters:
    - to_number: WhatsApp recipient in E.164 format, prefixed with 'whatsapp:'
                 e.g., 'whatsapp:+15551234567'
                 If the caller passes a bare phone (+1555...), we will prefix automatically.
    - message: Text content to send.

    Notes:
    - For Twilio sandbox, the recipient must join your sandbox first.
    - For a WhatsApp Business-approved number, ensure templates and opt-in are configured.
    """
    try:
        # Ensure proper whatsapp: prefix on recipient
        to_addr = to_number if str(to_number).startswith("whatsapp:") else f"whatsapp:{to_number}"

        msg = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_FROM,
            to=to_addr
        )
        print(f"WhatsApp message sent to {to_addr}: SID {msg.sid}")
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp message to {to_number}: {e}")
        return False


def notify_owner_or_tenant_via_whatsapp(recipient_number, subject, body):
    """
    Convenience helper to format and send a WhatsApp notification to an owner/tenant.

    recipient_number: phone in E.164 (e.g., +15551234567) or already prefixed 'whatsapp:+15551234567'
    subject: short subject/title of the notification
    body: main message body

    Returns True on success, False otherwise.
    """
    message = f"{subject}\n\n{body}"
    return send_whatsapp(recipient_number, message)
