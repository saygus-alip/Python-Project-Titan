import customtkinter as ctk
from user_database import UserDatabase
from tkinter import messagebox


class UserManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = UserDatabase()

        self.title("User Management System")
        self.geometry("800x600")

        # Set up a grid layout for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Frame for controls (Add, Update, Delete)
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Frame for user list
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.setup_control_widgets()
        self.setup_user_list_widgets()
        self.refresh_user_list()

    def setup_control_widgets(self):
        self.control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.username_label = ctk.CTkLabel(self.control_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ctk.CTkEntry(self.control_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.password_label = ctk.CTkLabel(self.control_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(self.control_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.add_button = ctk.CTkButton(self.control_frame, text="Add User", command=self.add_user_handler)
        self.add_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.update_button = ctk.CTkButton(self.control_frame, text="Update Password",
                                           command=self.update_password_handler)
        self.update_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        self.delete_button = ctk.CTkButton(self.control_frame, text="Delete User", command=self.delete_user_handler,
                                           fg_color="red")
        self.delete_button.grid(row=0, column=3, rowspan=2, padx=10, pady=5, sticky="nsew")

    def setup_user_list_widgets(self):
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)

        self.user_list_label = ctk.CTkLabel(self.list_frame, text="All Users", font=ctk.CTkFont(size=16, weight="bold"))
        self.user_list_label.grid(row=0, column=0, padx=10, pady=10)

        self.user_listbox = ctk.CTkScrollableFrame(self.list_frame)
        self.user_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # This will hold the labels for each user
        self.user_labels = {}

    def refresh_user_list(self):
        # Clear existing labels
        for widget in self.user_listbox.winfo_children():
            widget.destroy()

        self.user_labels.clear()

        users = self.db.get_all_users()

        if not users:
            no_user_label = ctk.CTkLabel(self.user_listbox, text="No users found.", font=ctk.CTkFont(size=14))
            no_user_label.pack(pady=20, padx=20)
            return

        for i, user in enumerate(users):
            user_id, username, expiry_date = user
            label_text = f"ID: {user_id:<4} | Username: {username:<15} | Expiry: {expiry_date}"

            user_label = ctk.CTkLabel(self.user_listbox, text=label_text, justify="left")
            user_label.pack(fill="x", padx=10, pady=5)
            self.user_labels[username] = user_label

    def add_user_handler(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        success = self.db.add_user(username, password)
        if success:
            messagebox.showinfo("Success", f"User '{username}' added successfully.")
            self.refresh_user_list()
            self.clear_entries()

    def update_password_handler(self):
        username = self.username_entry.get()
        new_password = self.password_entry.get()

        if not username or not new_password:
            messagebox.showerror("Error", "Username and new password cannot be empty.")
            return

        success = self.db.update_password(username, new_password)
        if success:
            messagebox.showinfo("Success", f"Password for user '{username}' updated.")
            self.refresh_user_list()
            self.clear_entries()
        else:
            messagebox.showerror("Error", f"User '{username}' not found.")

    def delete_user_handler(self):
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Please enter a username to delete.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            success = self.db.delete_user(username)
            if success:
                messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                self.refresh_user_list()
                self.clear_entries()
            else:
                messagebox.showerror("Error", f"User '{username}' not found.")

    def clear_entries(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')


if __name__ == "__main__":
    app = UserManagementApp()
    app.mainloop()