import customtkinter as ctk
from tkinter import messagebox
import os
import threading
import time
from plyer import notification

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TaskDetailsDialog(ctk.CTkToplevel):
    def __init__(self, parent, task_text, current_details):
        super().__init__(parent)
        self.title("Task Details")
        self.geometry("350x250")
        self.task_text = task_text
        self.details = current_details

        self.label = ctk.CTkLabel(self, text=f"Details for: {self.task_text}", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, height=100)
        self.textbox.insert("0.0", self.details)
        self.textbox.pack(padx=10, pady=5, fill="both", expand=True)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_details)
        self.save_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.transient(parent)
        self.grab_set()

    def save_details(self):
        self.details = self.textbox.get("1.0", "end-1c")
        self.master.update_task_details(self.task_text, self.details)
        self.destroy()

    def on_close(self):
        self.grab_release()
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Custom To-Do List")
        self.geometry("450x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label = ctk.CTkLabel(self.main_frame, text="My To-Do List", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=10)

        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(pady=5, padx=10, fill="x")

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Enter a new task...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.add_button = ctk.CTkButton(input_frame, text="Add", width=70, command=self.add_task)
        self.add_button.pack(side="right", padx=5)

        self.tasks_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.tasks_frame.pack(pady=10, padx=10, fill="both", expand=True)

        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.pack(pady=5, padx=10, fill="x")

        self.set_reminder_button = ctk.CTkButton(control_frame, text="Set Reminder", command=self.set_reminder)
        self.set_reminder_button.pack(side="left", padx=5, expand=True)

        self.remove_button = ctk.CTkButton(control_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side="left", padx=5, expand=True)

        self.clear_button = ctk.CTkButton(control_frame, text="Clear All", command=self.clear_tasks)
        self.clear_button.pack(side="left", padx=5, expand=True)

        self.tasks = {}
        self.task_widgets = {}

        self.load_tasks()

    def add_task(self):
        task_text = self.entry.get()
        if task_text:
            self.create_task_widget(task_text, False)
            self.entry.delete(0, "end")
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        selected_tasks = [task_text for task_text, (task_frame, checkbox, _, _) in self.task_widgets.items() if
                          checkbox.get() == 1]

        if not selected_tasks:
            messagebox.showwarning("Warning", "Please select a task to remove.")
            return

        for task_text in selected_tasks:
            self.task_widgets[task_text][0].destroy()
            del self.task_widgets[task_text]
            del self.tasks[task_text]

        self.save_tasks()

    def create_task_widget(self, task_text, is_completed, details=""):
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(pady=2, padx=5, fill="x")

        checkbox = ctk.CTkCheckBox(task_frame, text=task_text, font=("Arial", 12), command=self.save_tasks)
        checkbox.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        if is_completed:
            checkbox.select()

        # New: Add Details Button
        details_button = ctk.CTkButton(task_frame, text="Add Details", width=50,
                                       command=lambda: self.add_details(task_text))
        details_button.pack(side="right", padx=5)

        self.tasks[task_text] = {"details": details, "completed": is_completed}
        self.task_widgets[task_text] = (task_frame, checkbox, details_button)

    def add_details(self, task_text):
        current_details = self.tasks.get(task_text, {}).get("details", "")
        dialog = TaskDetailsDialog(self, task_text, current_details)
        self.wait_window(dialog)

    def update_task_details(self, task_text, details):
        if task_text in self.tasks:
            self.tasks[task_text]["details"] = details
            self.save_tasks()

    def set_reminder(self):
        selected_tasks = [task_text for task_text, (task_frame, checkbox, _) in self.task_widgets.items() if
                          checkbox.get() == 1]

        if not selected_tasks:
            messagebox.showwarning("Warning", "Please select a task to set a reminder.")
            return

        try:
            reminder_minutes = int(
                ctk.CTkInputDialog(text="Enter reminder time in minutes:", title="Set Reminder").get_input())
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please enter a number.")
            return

        for task_text in selected_tasks:
            thread = threading.Thread(target=self.schedule_notification, args=(task_text, reminder_minutes * 60))
            thread.daemon = True
            thread.start()

        messagebox.showinfo("Success", f"Reminder set for selected tasks in {reminder_minutes} minutes.")

    def schedule_notification(self, task_text, delay_seconds):
        time.sleep(delay_seconds)
        details = self.tasks.get(task_text, {}).get("details", "")
        notification_message = f"It's time to do: {task_text}"
        if details:
            notification_message += f"\nDetails: {details}"
        notification.notify(
            title="To-Do List Reminder",
            message=notification_message,
            app_name="Custom To-Do List"
        )

    def save_tasks(self):
        with open("tasks.txt", "w", encoding="utf-8") as f:
            for task_text, task_data in self.tasks.items():
                is_completed = task_data.get("completed", False)
                details = task_data.get("details", "")
                f.write(f"{task_text}|{is_completed}|{details}\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        task_text = parts[0]
                        is_completed = parts[1] == "1"
                        details = parts[2] if len(parts) > 2 else ""

                        self.create_task_widget(task_text, is_completed, details)

    def clear_tasks(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
            for task_frame in self.tasks_frame.winfo_children():
                task_frame.destroy()
            self.tasks.clear()
            self.task_widgets.clear()
            self.save_tasks()


if __name__ == "__main__":
    app = App()
    app.mainloop()