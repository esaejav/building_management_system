import tkinter as tk
from tkinter import ttk, messagebox
from db import add_owner_tenant, get_all_owners_tenants, update_owner_tenant, delete_owner_tenant

class EntryManagement(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Manage Owners/Tenants")
        self.geometry("900x400")
        self.id_selected = None

        # Form Labels and Inputs
        labels = ["Name", "Flat/Unit No", "Contact", "Ownership Type", "WhatsApp No"]
        for i, text in enumerate(labels):
            tk.Label(self, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")

        self.name_var = tk.StringVar()
        self.flat_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.ownership_var = tk.StringVar()
        self.whatsapp_var = tk.StringVar()

        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(self, textvariable=self.flat_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(self, textvariable=self.contact_var).grid(row=2, column=1, padx=5, pady=5)

        self.ownership_cb = ttk.Combobox(self, textvariable=self.ownership_var, values=["Owner", "Tenant"], state="readonly")
        self.ownership_cb.grid(row=3, column=1, padx=5, pady=5)
        self.ownership_cb.current(0)

        tk.Entry(self, textvariable=self.whatsapp_var).grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self, text="Add", command=self.add_entry).grid(row=5, column=0, pady=10)
        tk.Button(self, text="Update", command=self.update_entry).grid(row=5, column=1, pady=10)
        tk.Button(self, text="Delete", command=self.delete_entry).grid(row=5, column=2, pady=10)
        tk.Button(self, text="Clear", command=self.clear_form).grid(row=5, column=3, pady=10)

        # Treeview listing owners/tenants
        columns = ("ID", "Name", "Flat/Unit", "Contact", "Ownership", "WhatsApp")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.load_entries()

    def load_entries(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in get_all_owners_tenants():
            self.tree.insert("", "end", values=row)

    def add_entry(self):
        name = self.name_var.get().strip()
        flat = self.flat_var.get().strip()
        contact = self.contact_var.get().strip()
        ownership = self.ownership_var.get()
        whatsapp = self.whatsapp_var.get().strip()

        if not name or not flat or not ownership:
            messagebox.showerror("Error", "Fields Name, Flat/Unit, and Ownership are required.")
            return
        add_owner_tenant(name, flat, contact, ownership, whatsapp)
        messagebox.showinfo("Success", "Owner/Tenant added.")
        self.load_entries()
        self.clear_form()

    def update_entry(self):
        if self.id_selected is None:
            messagebox.showerror("Error", "Select an entry to update.")
            return
        name = self.name_var.get().strip()
        flat = self.flat_var.get().strip()
        contact = self.contact_var.get().strip()
        ownership = self.ownership_var.get()
        whatsapp = self.whatsapp_var.get().strip()

        if not name or not flat or not ownership:
            messagebox.showerror("Error", "Fields Name, Flat/Unit, and Ownership are required.")
            return
        update_owner_tenant(self.id_selected, name, flat, contact, ownership, whatsapp)
        messagebox.showinfo("Success", "Owner/Tenant updated.")
        self.load_entries()
        self.clear_form()

    def delete_entry(self):
        if self.id_selected is None:
            messagebox.showerror("Error", "Select an entry to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            delete_owner_tenant(self.id_selected)
            messagebox.showinfo("Deleted", "Entry deleted.")
            self.load_entries()
            self.clear_form()

    def clear_form(self):
        self.id_selected = None
        self.name_var.set("")
        self.flat_var.set("")
        self.contact_var.set("")
        self.ownership_cb.current(0)
        self.whatsapp_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.id_selected = values[0]
            self.name_var.set(values[1])
            self.flat_var.set(values[2])
            self.contact_var.set(values[3])
            self.ownership_var.set(values[4])
            self.whatsapp_var.set(values[5])
