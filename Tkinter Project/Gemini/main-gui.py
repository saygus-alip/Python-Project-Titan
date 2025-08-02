import customtkinter as ctk
import google.generativeai as genai
import threading
import queue

# --- Gemini API Configuration ---
# Replace 'YOUR_API_KEY' with your actual API key
genai.configure(api_key="AIzaSyAQ3pPGNeoQlrihus9g_U9OVbcRerscWRo")

# --- Global variables for the model ---
model = None
response_queue = queue.Queue()


# --- Functions for a smooth user experience ---
def check_model_availability():
    """Checks for available Gemini models and sets up the model."""
    global model
    try:
        status_label.configure(text="Status: Checking for models...", text_color="yellow")
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

        # Prioritize gemini-1.0-pro as a stable free tier model
        if 'models/gemini-1.0-pro' in available_models:
            model = genai.GenerativeModel('gemini-1.0-pro')
            status_label.configure(text="Status: Gemini 1.0 Pro is ready.", text_color="lightgreen")
        # Fallback to other available models if gemini-1.0-pro is not found
        elif 'models/gemini-1.5-pro-latest' in available_models:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            status_label.configure(text="Status: Gemini 1.5 Pro is ready.", text_color="lightgreen")
        else:
            status_label.configure(text="Error: No supported Gemini model found.", text_color="red")

    except Exception as e:
        status_label.configure(text=f"Error checking models: {e}", text_color="red")


def get_gemini_response_in_thread(user_input):
    """Sends user input to Gemini in a separate thread to prevent UI freezing."""
    try:
        response = model.generate_content(user_input)
        response_queue.put(response.text)
    except Exception as e:
        response_queue.put(f"Error: {e}")


def update_ui_with_response():
    """Checks the queue and updates the UI with the Gemini response."""
    try:
        response = response_queue.get(block=False)
        chat_history.configure(state="normal")
        chat_history.insert(ctk.END, f"Gemini: {response}\n\n", "gemini_tag")
        chat_history.configure(state="disabled")
        chat_history.see(ctk.END)
        chat_entry.configure(state="normal")
        send_button.configure(state="normal")
    except queue.Empty:
        root.after(100, update_ui_with_response)


def handle_user_input():
    """Handles user input and starts the response generation process."""
    user_input = chat_entry.get()

    if user_input and model:
        chat_history.configure(state="normal")
        chat_history.insert(ctk.END, f"You: {user_input}\n", "user_tag")
        chat_history.configure(state="disabled")

        chat_entry.delete(0, ctk.END)
        chat_entry.configure(state="disabled")
        send_button.configure(state="disabled")

        response_thread = threading.Thread(target=get_gemini_response_in_thread, args=(user_input,))
        response_thread.start()

        update_ui_with_response()
    elif not model:
        chat_history.configure(state="normal")
        chat_history.insert(ctk.END, "Error: Model not loaded. Check API Key and internet connection.\n", "error_tag")
        chat_history.configure(state="disabled")


# --- Main Window Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Gemini Chatbot")
root.geometry("500x500")

# --- Create UI Widgets ---
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

status_label = ctk.CTkLabel(main_frame, text="Status: Checking for models...", font=("Helvetica", 12))
status_label.pack(pady=(0, 5))

chat_history = ctk.CTkTextbox(main_frame, state="disabled", font=("Helvetica", 14))
chat_history.pack(fill=ctk.BOTH, expand=True, pady=(0, 10))

chat_history.tag_config("user_tag", foreground="lightblue")
chat_history.tag_config("gemini_tag", foreground="lightgreen")
chat_history.tag_config("error_tag", foreground="red")

input_frame = ctk.CTkFrame(main_frame)
input_frame.pack(fill=ctk.X)

chat_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your question here...", font=("Helvetica", 14))
chat_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 5))
chat_entry.bind("<Return>", lambda event=None: handle_user_input())

send_button = ctk.CTkButton(input_frame, text="Send", command=handle_user_input, font=("Helvetica", 14, "bold"))
send_button.pack(side=ctk.RIGHT)

# --- Start the model check and the main loop ---
check_model_availability()
root.mainloop()