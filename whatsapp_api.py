import pywhatkit

def send_whatsapp_group_message(group_id, message):
    try:
        pywhatkit.sendwhatmsg_to_group_instantly(group_id, message)
        print(f"WhatsApp message sent to group {group_id}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

