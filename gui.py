import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import random #Pause to add better typing effect
import google.generativeai as genai
import json
import socket
from PIL import Image, ImageTk

# Initialize System information (nothing bad I swear)
hostname = socket.gethostname()

# Window
app = ctk.CTk()
app.title("Ivy")
app.geometry('600x400')

# Get screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.resizable(True, True)
app.minsize(300, 300)

ctk.set_default_color_theme("blue")

ctk.deactivate_automatic_dpi_awareness()

# Initialize AI model

with open('api_key.txt', 'r') as key:
    content = key.read()

genai.configure(api_key=content)

with open('creator_info.txt', 'r') as file:
    aboutme = file.readlines()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=aboutme
)

chat_history_file = "chat_history.json"

def load_history():
    try:
        with open(chat_history_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error in gui.py: ", e)

def save_history(history): #GOD I HATE THIS PART HOW DO I MAKE IT SAVE
    try: #actually try this time pls 🙏
        with open(chat_history_file, 'w') as file:
            json.dump(history, file)
    except Exception as e:
        print("Error in gui.py: ", e)

    # If it SOMEHOW doesn't get the json contents, history will just stay blank
try: #PLEEEEEEEASEEEE
    with open(chat_history_file, 'r') as file:
        history = json.load(file)
except (FileNotFoundError) as e:
    history = []
    print("Error in gui.py: ", e, "\nHistory could not be retrieved.")


# Classes and Functions


def send(event):
    message = entry_widget.get()
    if not message.strip():
        return
    entry_widget.delete(0, tk.END)  # Clear the entry field
    response_widget.configure(text="")  # Clear the label before typing effect
    type_effect(response_widget, message, 0)  # Start typing effect

def type_effect(response_widget, text, idx):
    if idx < len(text):
        current_text = response_widget.cget("text")  # Get current text
        response_widget.configure(text=current_text + text[idx])  # Update label text
        
        # Determine the delay based on the character
        if text[idx] in [' ', '.', ',', '?','!','@', '$', '&', '*', ')']:
            # Longer delay for spaces and periods
            delay = random.randint(200, 500)  # Random delay between 200 and 500 ms
        else:
            # Shorter delay for other characters
            delay = random.randint(50, 150)  # Random delay between 50 and 150 ms
        
        # Call the function again after the delay
        response_widget.after(delay, type_effect, response_widget, text, idx + 1)

def update_label():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date_widget.configure(text=current_time)
    app.after(500, update_label)

# App content

    # Tabs
tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

home_tab = tabview.add("Home")
chat_tab = tabview.add("Chat")
settings_tab = tabview.add("Settings")

home_btn = ctk.CTkButton(home_tab)
home_btn.grid(row=0, column=0, padx=20, pady=10)

    # Home content
date_widget = ctk.CTkLabel(home_tab, font=("Times New Roman", 28))
date_widget.grid(padx=0, pady=50)

    # Chat content
response_widget = ctk.CTkLabel(chat_tab, text=f"Welcome back, {hostname}", font=("Helvetica", 16))
response_widget.grid(row=0, column=0, padx=20, pady=20)

entry_widget = ctk.CTkEntry(chat_tab, placeholder_text="Talk to Ivy...")
entry_widget.grid(row=0, column=0, padx=20, pady=30)

    # Settings content
dark_mode = False

def dark_mode_switch():
    global dark_mode
    dark_mode = not dark_mode
    ctk.set_appearance_mode('dark' if dark_mode else 'light')
    print("gui.py: appearance mode changed!")



settings_btn = ctk.CTkButton(settings_tab, text = 'Activate light mode' if dark_mode else 'Activate dark mode' ,command=dark_mode_switch)
settings_btn.grid(row = 0, column = 0, padx=20, pady=20)

    # Bind the Return key to the send function
entry_widget.bind('<Return>', send)  # Pass the function reference without parentheses

update_label()

app.mainloop()