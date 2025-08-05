# Python Building Management System

## Features
- Admin login with secure password hashing
- Manage owners and tenants (CRUD)
- Track monthly maintenance payments
- Automated SMS reminders for unpaid maintenance (6th-8th)
- WhatsApp group notification on unpaid dues (9th)
- Simple Tkinter GUI and SQLite backend

## Setup Instructions

1. Clone or download the project.
2. Create a virtual environment and activate it.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Setup database tables:
    ```
    python -c "from db import setup_tables; setup_tables()"
    ```
5. Create admin user:
    ```
    python create_admin_user.py
    ```
6. Run the app:
    ```
    python main.py
    ```
7. Run automated reminders in a separate terminal:
    ```
    python scheduler.py
    ```

## Notes
- Configure Twilio credentials in `sms_api.py`
- Configure WhatsApp group ID in `scheduler.py`
- Ensure WhatsApp Web session is active for pywhatkit to send messages
