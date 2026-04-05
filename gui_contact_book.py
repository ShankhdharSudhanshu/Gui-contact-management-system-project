import tkinter as tk
from tkinter import messagebox
import json

# Contact Class (UNCHANGED ✅)
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"


# Contact Book Class (UNCHANGED ✅)
class ContactBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, name, phone, email):
        self.contacts[name] = Contact(name, phone, email)
        print(f"✅ Contact '{name}' added successfully!")

    def view_contacts(self):
        if not self.contacts:
            print("❌ No contacts found!")
        else:
            for contact in self.contacts.values():
                print(contact)

    def search_contact(self, name):
        contact = self.contacts.get(name)
        if contact:
            return contact
        return None

    def update_contact(self, name, phone=None, email=None):
        if name in self.contacts:
            if phone:
                self.contacts[name].phone = phone
            if email:
                self.contacts[name].email = email
            print(f"✅ Contact '{name}' updated successfully!")
        else:
            print("❌ Contact not found!")

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            print(f"🗑 Contact '{name}' deleted successfully!")
        else:
            print("❌ Contact not found!")

    def save_to_file(self, filename="contacts.json"):
        with open(filename, "w") as file:
            json.dump(
                {name: vars(contact) for name, contact in self.contacts.items()},
                file,
                indent=4
            )
        print("💾 Contacts saved successfully!")

    def load_from_file(self, filename="contacts.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.contacts = {
                    name: Contact(**info) for name, info in data.items()
                }
                print("📂 Contacts loaded successfully!")
        except FileNotFoundError:
            print("❌ No saved contacts found!")


# GUI CLASS
class ContactGUI:
    def __init__(self, root):
        self.book = ContactBook()
        self.book.load_from_file()

        self.root = root
        self.root.title("📒 Contact Book GUI")
        self.root.geometry("450x550")
        self.root.configure(bg="#121212")

        # Input Fields
        self.name_entry = tk.Entry(root, bg="#1e1e1e", fg="white")
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Name")

        self.phone_entry = tk.Entry(root, bg="#1e1e1e", fg="white")
        self.phone_entry.pack(pady=5)
        self.phone_entry.insert(0, "Phone")

        self.email_entry = tk.Entry(root, bg="#1e1e1e", fg="white")
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "Email")

        # Buttons
        tk.Button(root, text="➕ Add", command=self.add_contact).pack(pady=5)
        tk.Button(root, text="🔍 Search", command=self.search_contact).pack(pady=5)
        tk.Button(root, text="✏ Update", command=self.update_contact).pack(pady=5)
        tk.Button(root, text="❌ Delete", command=self.delete_contact).pack(pady=5)
        tk.Button(root, text="💾 Save", command=self.save_contacts).pack(pady=5)

        # Listbox
        self.listbox = tk.Listbox(root, width=50, bg="#1e1e1e", fg="white")
        self.listbox.pack(pady=10)

        self.load_listbox()

    # GUI FUNCTIONS (Using SAME backend methods ✅)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        self.book.add_contact(name, phone, email)
        self.load_listbox()

    def search_contact(self):
        name = self.name_entry.get()
        contact = self.book.search_contact(name)

        if contact:
            messagebox.showinfo("Found", str(contact))
        else:
            messagebox.showerror("Error", "Contact not found")

    def update_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        self.book.update_contact(
            name,
            phone if phone else None,
            email if email else None
        )
        self.load_listbox()

    def delete_contact(self):
        name = self.name_entry.get()
        self.book.delete_contact(name)
        self.load_listbox()

    def save_contacts(self):
        self.book.save_to_file()
        messagebox.showinfo("Saved", "Contacts saved successfully")

    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in self.book.contacts.values():
            self.listbox.insert(tk.END, str(contact))


# RUN GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactGUI(root)
    root.mainloop()