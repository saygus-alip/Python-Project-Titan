# C:\Users\tcham\PythonProject\Python-Project-Titan\Game\Game_Core.py

class Game:
    def __init__(self):
        self.score = 0
        self.health = 100

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        print(f"Game: Score changed from {self.score} to {new_score}")
        self.score = new_score

    def get_health(self):
        return self.health

    def set_health(self, new_health):
        print(f"Game: Health changed from {self.health} to {new_health}")
        self.health = new_health

# สร้าง Instance ของเกมขึ้นมาเพื่อใช้งาน
# ไฟล์อื่นๆ สามารถ import ตัวแปร game_instance นี้ไปได้เลย
Game_Instance = Game()