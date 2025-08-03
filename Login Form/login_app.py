import customtkinter as ctk
from user_database import UserDatabase
from user_management_app import UserManagementApp
from tkinter import messagebox


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = UserDatabase()

        self.title("Login")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.login_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        # We need to bind the <Return> key to the login function for better user experience
        self.bind('<Return>', self.login_on_enter)

    def login_on_enter(self, event):
        self.login()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.check_user(username, password):
            if self.db.is_logged_in(username):
                messagebox.showerror("Login Error", "This user is already logged in on another device.")
            else:
                self.db.set_login_status(username, 1)  # Set user as logged in
                messagebox.showinfo("Success", "Login successful!")
                self.destroy()  # Close the login window

                # Open the user management app
                user_management_app = UserManagementApp()
                user_management_app.mainloop()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")
            self.password_entry.delete(0, 'end')


if __name__ == "__main__":
    # Create a default user if none exist for testing purposes
    db_check = UserDatabase()
    users_exist = db_check.get_all_users()
    if not users_exist:
        db_check.add_user("admin", "admin123")
        print("Created a default 'admin' user with password 'admin123' for first-time use.")

    app = LoginApp()
    app.mainloop()