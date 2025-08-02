# C:\Users\tcham\PythonProject\Python-Project-Titan\Mod_Menu\main.py

import customtkinter
from Mod_Menu.Mod_Menu_UI import ModMenu  # แก้เป็นแบบนี้

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    app = ModMenu()
    app.mainloop()