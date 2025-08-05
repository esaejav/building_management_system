import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_all_owners_tenants, get_payment, add_payment, update_payment_status

class PaymentManagement(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Payments Management")
        self.geometry("900x400")

        tk.Label(self, text="Month (1-12):").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Year (YYYY):").grid(row=0, column=2, padx=5, pady=5)

        self.month_var = tk.IntVar(value=datetime.now().month)
        self.year_var = tk.IntVar(value=datetime.now().year)

        tk.Entry(self, textvariable=self.month_var, width=5).grid(row=0, column=1)
        tk.Entry(self, textvariable=self.year_var, width=7).grid(row=0, column=3)
        tk.Button(self, text="Load Payments", command=self.load_payments).grid(row=0, column=4, padx=10)

        cols = ("Payment ID", "Name", "Flat", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=1, column=0, columnspan=5, pady=10, padx=5, sticky='nsew')

        tk.Button(self, text="Mark as Paid", command=self.mark_paid).grid(row=2, column=2)

        self.load_payments()

    def load_payments(self):
        month = self.month_var.get()
        year = self.year_var.get()

        # Clear treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Ensure payment records for all owners/tenants for this month exist
        tenants = get_all_owners_tenants()
        for tenant in tenants:
            p = get_payment(tenant[0], month, year)
            if not p:
                add_payment(tenant[0], month, year)

        # Reload payment records
        conn = None
        try:
            # Directly use db function to get payments
            from db import get_all_payments_for_month
            payments = get_all_payments_for_month(year, month)

            for payment in payments:
                payment_id, name, flat_no, _, _, status, *_ = payment
                color = "#90EE90" if status == "Paid" else "#FFCCCB"
                self.tree.insert("", "end", values=(payment_id, name, flat_no, status), tags=(status,))
                self.tree.tag_configure('Paid', background="#D0F0C0")
                self.tree.tag_configure('Pending', background="#FFCCCC")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_paid(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a payment record.")
            return
        item = self.tree.item(selected[0])['values']
        payment_id = item[0]
        update_payment_status(payment_id, "Paid")
        messagebox.showinfo("Updated", "Payment marked as Paid.")
        self.load_payments()
