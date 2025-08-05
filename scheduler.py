import schedule
import time
from datetime import datetime
from db import get_all_payments_for_month, update_reminder_sent, update_payment_status
from sms_api import send_sms
from whatsapp_api import send_whatsapp_group_message

# Replace with your WhatsApp group id like '1201234567890-123456@g.us'
WHATSAPP_GROUP_ID = 'your_whatsapp_group_id@g.us'

def send_reminder(day):
    today = datetime.today()
    month = today.month
    year = today.year

    payments = get_all_payments_for_month(year, month)

    for payment in payments:
        payment_id, name, flat_no, contact, whatsapp, status, d6_sent, d7_sent, d8_sent = payment
        if status == "Pending":
            # Check if reminder sent already for this day
            reminder_sent = {6: d6_sent, 7: d7_sent, 8: d8_sent}
            if reminder_sent.get(day) == 0:
                # Send SMS if contact is available
                if contact:
                    msg = f"Dear {name}, your monthly maintenance fee for flat {flat_no} is pending. Please pay by 9th to avoid group notice."
                    if send_sms(contact, msg):
                        update_reminder_sent(payment_id, day)

def send_whatsapp_defaulters_notice():
    today = datetime.today()
    if today.day != 9:
        return

    month = today.month
    year = today.year
    payments = get_all_payments_for_month(year, month)

    defaulters = []
    for payment in payments:
        payment_id, name, flat_no, contact, whatsapp, status, *_ = payment
        if status == "Pending":
            defaulters.append(f"{name} (Flat {flat_no})")

    if defaulters:
        message = "Maintenance Payment Pending for the following flats:\n" + "\n".join(defaulters)
        message += "\nPlease make the payments at the earliest."
        send_whatsapp_group_message(WHATSAPP_GROUP_ID, message)

def job():
    day = datetime.today().day
    if day in [6, 7, 8]:
        print(f"Sending reminders for day {day}")
        send_reminder(day)
    elif day == 9:
        print("Sending WhatsApp defaulter notice")
        send_whatsapp_defaulters_notice()

schedule.every().day.at("10:00").do(job)

print("Scheduler started. Waiting for scheduled tasks...")
while True:
    schedule.run_pending()
    time.sleep(60)