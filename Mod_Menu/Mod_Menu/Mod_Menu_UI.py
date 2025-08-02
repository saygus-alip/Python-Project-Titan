# C:\Users\tcham\PythonProject\Python-Project-Titan\Mod_Menu\Mod_Menu_UI.py

import customtkinter

# ใช้ try-except เพื่อจัดการข้อผิดพลาดในการ import
try:
    from Game.Game_Core import Game_Instance
except ImportError:
    print("Error: The 'Game' module could not be imported. Please check your project structure.")
    print("Running in dummy mode. Mod menu functionality will be limited.")


    # ถ้า import ไม่สำเร็จ จะสร้าง class และ instance สำรองขึ้นมาแทน
    class DummyGame:
        def get_score(self):
            return 0

        def set_score(self, new_score):
            print("DummyGame: Score cannot be set.")

        def get_health(self):
            return 100

        def set_health(self, new_health):
            print("DummyGame: Health cannot be set.")


    Game_Instance = DummyGame()


class ModMenu(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Mod Menu")
        self.geometry("450x300")
        self.create_widgets()

    def create_widgets(self):
        # โค้ดส่วน UI ทั้งหมดจะเหมือนเดิม
        title_label = customtkinter.CTkLabel(self, text="GAME MOD MENU",
                                             font=customtkinter.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))

        score_frame = customtkinter.CTkFrame(self)
        score_frame.pack(pady=10, padx=10, fill="x")

        score_label = customtkinter.CTkLabel(score_frame, text="Score:", font=customtkinter.CTkFont(size=16))
        score_label.pack(side="left", padx=(10, 5))

        self.score_entry = customtkinter.CTkEntry(score_frame, placeholder_text="Enter new score...")
        self.score_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        update_score_button = customtkinter.CTkButton(score_frame, text="Set", command=self.update_score)
        update_score_button.pack(side="left", padx=(0, 10))

        health_frame = customtkinter.CTkFrame(self)
        health_frame.pack(pady=10, padx=10, fill="x")

        health_label = customtkinter.CTkLabel(health_frame, text="Health:", font=customtkinter.CTkFont(size=16))
        health_label.pack(side="left", padx=(10, 5))

        self.health_entry = customtkinter.CTkEntry(health_frame, placeholder_text="Enter new health...")
        self.health_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        update_health_button = customtkinter.CTkButton(health_frame, text="Set", command=self.update_health)
        update_health_button.pack(side="left", padx=(0, 10))

        self.status_label = customtkinter.CTkLabel(self,
                                                   text=f"Current Score: {Game_Instance.get_score()} | Health: {Game_Instance.get_health()}",
                                                   font=customtkinter.CTkFont(size=14))
        self.status_label.pack(pady=15)

    def update_score(self):
        try:
            new_score = int(self.score_entry.get())
            Game_Instance.set_score(new_score)
            self.update_status_label()
        except ValueError:
            print("Invalid score input. Please enter a number.")

    def update_health(self):
        try:
            new_health = int(self.health_entry.get())
            Game_Instance.set_health(new_health)
            self.update_status_label()
        except ValueError:
            print("Invalid health input. Please enter a number.")

    def update_status_label(self):
        self.status_label.configure(
            text=f"Current Score: {Game_Instance.get_score()} | Health: {Game_Instance.get_health()}")