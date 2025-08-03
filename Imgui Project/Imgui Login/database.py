# database.py

import sqlite3
import bcrypt


class DatabaseManager:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the users table if it doesn't exist."""
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY,
                                username
                                TEXT
                                NOT
                                NULL
                                UNIQUE,
                                password
                                TEXT
                                NOT
                                NULL
                            )
                            ''')
        self.conn.commit()

    def register_user(self, username, password):
        """Registers a new user (with hashed password)."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                (username, hashed_password))
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def login_user(self, username, password):
        """Checks user login credentials."""
        self.cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()

        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return True, "Login successful!"
            else:
                return False, "Incorrect password."
        else:
            return False, "User not found."

    def close(self):
        """Closes the database connection."""
        self.conn.close()