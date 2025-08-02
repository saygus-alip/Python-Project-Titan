import customtkinter as ctk
import pyshorteners
import pyperclip

# ตั้งค่ารูปลักษณ์
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("URL Shortener")
root.geometry("400x400")
root.resizable(False, False)

# สร้าง Frame สำหรับวิดเจ็ต API Key
bitly_frame = ctk.CTkFrame(root, fg_color="transparent")

def update_ui(choice):
    """แสดงหรือซ่อนช่อง API Key ตามตัวเลือกบริการ"""
    if choice == "Bitly":
        bitly_frame.pack(pady=5)
    else:
        bitly_frame.pack_forget()
    root.update_idletasks()

def shorten():
    long_url = longurl_entry.get()
    service = service_option.get()

    if not long_url:
        shorturl_entry.configure(state="normal")
        shorturl_entry.delete(0, ctk.END)
        shorturl_entry.insert(0, "Please enter a URL")
        shorturl_entry.configure(state="readonly")
        return

    # ทำให้ช่อง Output สามารถเขียนได้ชั่วคราว
    shorturl_entry.configure(state="normal")
    shorturl_entry.delete(0, ctk.END)
    shorturl_entry.insert(0, "Processing")
    root.update_idletasks()

    try:
        shortener = pyshorteners.Shortener()
        short_url = None

        if service == "TinyURL":
            short_url = shortener.tinyurl.short(long_url)
        elif service == "Is.gd":
            short_url = shortener.isgd.short(long_url)
        elif service == "Chilp.it":
            try:
                short_url = shortener.chilpit.short(long_url)
            except pyshorteners.exceptions.ShorteningErrorException:
                short_url = "Error: Chilp.it failed. Please try another service."
        elif service == "Bitly":
            api_key = bitly_key_entry.get()
            if api_key:
                shortener = pyshorteners.Shortener(api_key=api_key)
                short_url = shortener.bitly.short(long_url)
            else:
                short_url = "Error: Please enter a Bitly API Key."

        shorturl_entry.delete(0, ctk.END)
        if short_url:
            shorturl_entry.insert(0, short_url)
        else:
            shorturl_entry.insert(0, "Error: Could not shorten URL.")

    except Exception as e:
        shorturl_entry.delete(0, ctk.END)
        shorturl_entry.insert(0, f"Error: {e}")

    # ตั้งค่าช่อง Output ให้เป็น Read-only อีกครั้ง
    shorturl_entry.configure(state="readonly")

def copy_to_clipboard():
    short_url = shorturl_entry.get()
    if short_url and "Error" not in short_url and "Please" not in short_url and "Processing" not in short_url:
        try:
            pyperclip.copy(short_url)
            # ทำให้ช่อง Output สามารถเขียนได้ชั่วคราว
            shorturl_entry.configure(state="normal")
            shorturl_entry.delete(0, ctk.END)
            shorturl_entry.insert(0, "URL copied to clipboard!")
            # ตั้งค่าช่อง Output ให้เป็น Read-only อีกครั้ง
            shorturl_entry.configure(state="readonly")
        except Exception:
            shorturl_entry.configure(state="normal")
            shorturl_entry.delete(0, ctk.END)
            shorturl_entry.insert(0, "Error: Could not copy URL.")
            shorturl_entry.configure(state="readonly")

# ตัวเลือกบริการย่อลิงก์
service_options = ["TinyURL", "Is.gd", "Chilp.it", "Bitly"]

# วิดเจ็ตต่างๆ
longurl_label = ctk.CTkLabel(root, text="Enter Long URL")
longurl_entry = ctk.CTkEntry(root, width=300)
service_label = ctk.CTkLabel(root, text="Choose Service")
service_option = ctk.CTkOptionMenu(root, values=service_options, command=update_ui)

# วิดเจ็ตสำหรับ Bitly API Key
bitly_key_label = ctk.CTkLabel(bitly_frame, text="Bitly API Key")
bitly_key_entry = ctk.CTkEntry(bitly_frame, width=300, show="*")

# วิดเจ็ตอื่นๆ
shorten_button = ctk.CTkButton(root, text="Shorten URL", command=shorten)
shorturl_label = ctk.CTkLabel(root, text="Output shortened URL")
shorturl_entry = ctk.CTkEntry(root, width=300, state="readonly")  # ตั้งค่าเริ่มต้นเป็น Read-only
copy_button = ctk.CTkButton(root, text="Copy URL", command=copy_to_clipboard)

# จัดวางวิดเจ็ต
longurl_label.pack(pady=(10, 0))
longurl_entry.pack(pady=5)
service_label.pack(pady=(5, 0))
service_option.pack(pady=5)
bitly_key_label.pack(pady=(5, 0))
bitly_key_entry.pack(pady=5)
bitly_frame.pack_forget()
shorten_button.pack(pady=5)
shorturl_label.pack(pady=(10, 0))
shorturl_entry.pack(pady=5)
copy_button.pack(pady=5)

root.mainloop()