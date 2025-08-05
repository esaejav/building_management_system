import tkinter as tk
from tkinter import messagebox
import bcrypt
from db import get_user_password

class LoginWindow(tk.Tk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("Login - Building Management System")
        self.geometry("300x150")

        tk.Label(self, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().encode('utf-8')

        stored_hash = get_user_password(username)
        if stored_hash and bcrypt.checkpw(password, stored_hash):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.destroy()
            self.on_success(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
