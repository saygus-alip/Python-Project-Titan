import customtkinter
from tkinter import messagebox
import pymem
import pymem.exception

# ตั้งค่า Apperance ของ CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class ModMenu(customtkinter.CTk):
    def __init__(self, game_name):
        super().__init__()
        self.game_name = game_name
        self.pm = None

        self.title(f"Mod Menu for {self.game_name}")
        self.geometry("400x350")
        self.create_widgets()

    def create_widgets(self):
        # Frame สำหรับการเชื่อมต่อ
        connect_frame = customtkinter.CTkFrame(self)
        connect_frame.pack(pady=10, padx=10, fill="x")

        self.connect_button = customtkinter.CTkButton(
            connect_frame, text=f"Connect to {self.game_name}", command=self.connect_to_game
        )
        self.connect_button.pack(side="left", padx=(10, 5), expand=True)

        self.status_label = customtkinter.CTkLabel(
            connect_frame, text="Status: Disconnected", text_color="red"
        )
        self.status_label.pack(side="left", padx=(5, 10))

        # Frame สำหรับ Address
        address_frame = customtkinter.CTkFrame(self)
        address_frame.pack(pady=5, padx=10, fill="x")

        customtkinter.CTkLabel(address_frame, text="Memory Address:").pack(side="left", padx=10)
        self.address_entry = customtkinter.CTkEntry(address_frame,
                                                    placeholder_text="Enter Hex Address (e.g., 12345678)")
        self.address_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        # Frame สำหรับ Value (String/Number)
        value_frame = customtkinter.CTkFrame(self)
        value_frame.pack(pady=5, padx=10, fill="x")

        customtkinter.CTkLabel(value_frame, text="New Value:").pack(side="left", padx=10)
        self.value_entry = customtkinter.CTkEntry(value_frame, placeholder_text="Enter new value or text")
        self.value_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        # Radio Buttons สำหรับเลือกประเภทข้อมูล
        self.value_type = customtkinter.StringVar(value="string")
        string_radio = customtkinter.CTkRadioButton(self, text="String (Text)", variable=self.value_type,
                                                    value="string")
        string_radio.pack(pady=5)
        int_radio = customtkinter.CTkRadioButton(self, text="Number (Int)", variable=self.value_type, value="int")
        int_radio.pack(pady=5)

        # ปุ่มสำหรับแก้ไขค่า
        self.set_value_button = customtkinter.CTkButton(
            self, text="Set Value", command=self.set_value
        )
        self.set_value_button.pack(pady=10)

    def connect_to_game(self):
        """เชื่อมต่อกับ Notepad และอัปเดตสถานะ"""
        try:
            self.pm = pymem.Pymem(self.game_name)
            self.status_label.configure(text=f"Status: Connected to {self.game_name}", text_color="green")
            messagebox.showinfo("Success", f"Successfully connected to {self.game_name}!")
        except pymem.exception.PymemError:
            self.pm = None
            self.status_label.configure(text="Status: Failed to connect", text_color="red")
            messagebox.showerror("Error", f"Could not connect to {self.game_name}. Make sure Notepad is running.")

    def set_value(self):
        """แก้ไขค่าใน Address ที่กำหนด"""
        if not self.pm:
            messagebox.showerror("Error", "Not connected to Notepad. Please connect first.")
            return

        try:
            address_str = self.address_entry.get()
            address = int(address_str, 16)
            new_value = self.value_entry.get()
            value_type = self.value_type.get()

            if value_type == "string":
                # แก้ไขเป็นข้อความ (String)
                self.pm.write_string(address, new_value)
                messagebox.showinfo("Success", f"Text at address {address_str} has been changed to '{new_value}'.")
            elif value_type == "int":
                # แก้ไขเป็นตัวเลข (Int)
                value = int(new_value)
                self.pm.write_int(address, value)
                messagebox.showinfo("Success", f"Number at address {address_str} has been changed to {value}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid hex address and a valid number/text.")
        except pymem.exception.PymemError:
            messagebox.showerror("Error", "Could not write to memory. Address may be incorrect or access denied.")


if __name__ == "__main__":
    game_name_to_mod = "notepad.exe"
    app = ModMenu(game_name_to_mod)
    app.mainloop()