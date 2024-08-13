import json
import os
import tkinter as tk
from tkinter import messagebox

class ContactBook:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, name, phone):
        self.contacts.append({'name': name, 'phone': phone})
        self.save_contacts()

    def delete_contact(self, name):
        self.contacts = [contact for contact in self.contacts if contact['name'] != name]
        self.save_contacts()

    def update_contact(self, old_name, new_name, new_phone):
        for contact in self.contacts:
            if contact['name'] == old_name:
                contact['name'] = new_name
                contact['phone'] = new_phone
                break
        self.save_contacts()

    def get_all_contacts(self):
        return self.contacts

class ContactBookGUI:
    def __init__(self, root, contact_book):
        self.root = root
        self.contact_book = contact_book
        self.root.title("Contact Book")

        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.phone_label = tk.Label(root, text="Phone:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(root)
        self.phone_entry.pack()

        self.old_name_label = tk.Label(root, text="Old Name (for update):")
        self.old_name_label.pack()
        self.old_name_entry = tk.Entry(root)
        self.old_name_entry.pack()

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.pack()

        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.update_button.pack()

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack()

        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts)
        self.view_button.pack()

        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.pack()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        if name and phone:
            self.contact_book.add_contact(name, phone)
            messagebox.showinfo("Success", f"Contact '{name}' added.")
        else:
            messagebox.showwarning("Input Error", "Please enter both name and phone.")

    def update_contact(self):
        old_name = self.old_name_entry.get()
        new_name = self.name_entry.get()
        new_phone = self.phone_entry.get()
        if old_name and new_name and new_phone:
            self.contact_book.update_contact(old_name, new_name, new_phone)
            messagebox.showinfo("Success", f"Contact '{old_name}' updated.")
        else:
            messagebox.showwarning("Input Error", "Please enter old name, new name, and new phone.")

    def delete_contact(self):
        name = self.name_entry.get()
        if name:
            self.contact_book.delete_contact(name)
            messagebox.showinfo("Success", f"Contact '{name}' deleted.")
        else:
            messagebox.showwarning("Input Error", "Please enter the name of the contact to delete.")

    def view_contacts(self):
        contacts = self.contact_book.get_all_contacts()
        self.result_text.delete(1.0, tk.END)
        for contact in contacts:
            self.result_text.insert(tk.END, f"Name: {contact['name']}, Phone: {contact['phone']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    contact_book = ContactBook()
    app = ContactBookGUI(root, contact_book)
    root.mainloop()
