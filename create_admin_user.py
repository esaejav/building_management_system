import bcrypt
from db import create_user, setup_tables

def create_admin(username, password):
    setup_tables()  # Ensure tables exist
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    if create_user(username, hashed):
        print(f"Admin user '{username}' created.")
    else:
        print(f"User '{username}' already exists.")

if __name__ == "__main__":
    # Change these as needed
    create_admin('admin', 'admin123')

