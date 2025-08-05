import tkinter as tk
from gui.entry_management import EntryManagement
from gui.payment_management import PaymentManagement

class Dashboard(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Dashboard - Building Management System")
        self.geometry("400x250")

        tk.Label(self, text=f"Welcome, {username}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self, text="Manage Owners/Tenants", width=30, command=self.open_entry_management).pack(pady=10)
        tk.Button(self, text="Manage Payments", width=30, command=self.open_payment_management).pack(pady=10)

    def open_entry_management(self):
        EntryManagement(self)

    def open_payment_management(self):
        PaymentManagement(self)

