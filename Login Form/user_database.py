import sqlite3
import hashlib
from datetime import datetime, timedelta


class UserDatabase:
    def __init__(self, db_file="user_db.sqlite"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                username
                                TEXT
                                UNIQUE
                                NOT
                                NULL,
                                password_hash
                                TEXT
                                NOT
                                NULL,
                                expiry_date
                                TEXT
                                NOT
                                NULL,
                                is_logged_in
                                INTEGER
                                DEFAULT
                                0
                            )
                            """)
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, expiry_days=90):
        # ตั้งวันหมดอายุของรหัสผ่านใน 90 วันข้างหน้า
        expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
        password_hash = self.hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, expiry_date) VALUES (?, ?, ?)",
                (username, password_hash, expiry_date)
            )
            self.conn.commit()
            print(f"User '{username}' added successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Username '{username}' already exists.")
            return False

    def check_user(self, username, password):
        password_hash = self.hash_password(password)
        self.cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        if result and result[0] == password_hash:
            return True
        return False

    def delete_user(self, username):
        self.cursor.execute(
            "DELETE FROM users WHERE username = ?",
            (username,)
        )
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully.")
            return True
        else:
            print(f"Error: User '{username}' not found.")
            return False

    def update_password(self, username, new_password, expiry_days=90):
        expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
        password_hash = self.hash_password(new_password)
        self.cursor.execute(
            "UPDATE users SET password_hash = ?, expiry_date = ? WHERE username = ?",
            (password_hash, expiry_date, username)
        )
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print(f"Password for user '{username}' updated successfully.")
            return True
        else:
            print(f"Error: User '{username}' not found.")
            return False

    def is_password_expired(self, username):
        self.cursor.execute(
            "SELECT expiry_date FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        if result:
            expiry_date_str = result[0]
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
            return datetime.now() > expiry_date
        return False  # ผู้ใช้ไม่พบหรือไม่หมดอายุ

    def set_login_status(self, username, status):
        # status: 1 = logged in, 0 = logged out
        self.cursor.execute(
            "UPDATE users SET is_logged_in = ? WHERE username = ?",
            (status, username)
        )
        self.conn.commit()

    def is_logged_in(self, username):
        self.cursor.execute(
            "SELECT is_logged_in FROM users WHERE username = ?",
            (username,)
        )
        result = self.cursor.fetchone()
        if result and result[0] == 1:
            return True
        return False

    def get_all_users(self):
        self.cursor.execute("SELECT id, username, expiry_date FROM users")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


# --- ตัวอย่างการใช้งาน ---
if __name__ == "__main__":
    db = UserDatabase()

    # 1. เพิ่มผู้ใช้ใหม่
    db.add_user("admin", "password123")
    db.add_user("user1", "userpass")

    print("\n--- แสดงผู้ใช้ทั้งหมด ---")
    users = db.get_all_users()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Expiry Date: {user[2]}")

    # 2. ทดสอบการเข้าสู่ระบบ
    print("\n--- ทดสอบการเข้าสู่ระบบ ---")
    if db.check_user("admin", "password123"):
        print("Login successful for 'admin'!")
        if not db.is_logged_in("admin"):
            db.set_login_status("admin", 1)
            print("'admin' is now logged in.")
        else:
            print("'admin' is already logged in on another device.")
    else:
        print("Invalid credentials for 'admin'.")

    if db.check_user("user1", "wrongpass"):
        print("Login successful for 'user1'!")
    else:
        print("Invalid credentials for 'user1'.")

    # 3. ทดสอบการเปลี่ยนรหัสผ่าน
    print("\n--- ทดสอบการเปลี่ยนรหัสผ่าน ---")
    db.update_password("user1", "new_user_pass")
    if db.check_user("user1", "new_user_pass"):
        print("Login successful with new password for 'user1'!")

    # 4. ทดสอบการลบผู้ใช้
    print("\n--- ทดสอบการลบผู้ใช้ ---")
    db.delete_user("user1")
    if not db.check_user("user1", "new_user_pass"):
        print("'user1' does not exist anymore.")

    # 5. ทดสอบการล็อกเอาท์
    print("\n--- ทดสอบการล็อกเอาท์ ---")
    db.set_login_status("admin", 0)
    if not db.is_logged_in("admin"):
        print("'admin' has been logged out.")