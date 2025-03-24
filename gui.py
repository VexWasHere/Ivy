import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import random #Pause to add better typing effect
import google.generativeai as genai
import json
import socket
from tkinter import messagebox
# import win32gui # Forgot what this was for ngl. Possibly notifications

default = 0
system_mode_on = True #Called beforehand to avoid confusion

# Initialize System information
hostname = socket.gethostname()

def show_alert(title, message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(title, message)


print(f"hostname")




# Window
app = ctk.CTk()
app.title("Ivy")
app.geometry('610x500')
app.iconbitmap('pixel_rose.ico')
app.configure(bg="#738290")


# Get screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

print(f"Dimensions: {screen_width}x{screen_height}")


app.resizable(True, True)
app.minsize(600, 400)
app.maxsize(800, 500)


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


chat = model.start_chat()


# Classes and Functions

def send():
    message = chat_input.get()
    if not message.strip():
        return
   
    try:
        chat_display.configure(state=tk.NORMAL)  # Enable editing
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.configure(state=tk.DISABLED)  # Disable editing


        response = chat.send_message(message) #old model
        chat_input.delete(0, tk.END)  # Clear the entry field
        #response_widget.configure(text="")  # Clear the label before typing effect
        response_text = wrap_text(response.text)


        chat_display.configure(state=tk.NORMAL)  # Enable editing
        chat_display.insert(tk.END, f"Ivy: {response_text}" + "\n")
        chat_display.configure(state=tk.DISABLED)  # Disable editing
    except Exception as e:
        print("Error in gui.py: ", e)


    # type_effect(response_widget, f"Ivy: {response_text}", 0)  # Start typing effect
    print("gui.py: Message sent")


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


def wrap_text(text, max_length=60):
    words = text.split()
    lines = []
    current_line = []


    for word in words:
        if sum(len(w) for w in current_line) + len(word) + len(current_line) <= max_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]


    if current_line:
        lines.append(' '.join(current_line))


    return '\n'.join(lines)


def update_label():
    #Give the time a little more life. As of now it is just a static time refreshed every hour on the hour.
    now = datetime.now()
    current_hour = now.hour
    greeting = "Good morning" if current_hour <= 12 else "Good evening"
    formatted_time = now.strftime('%I %p')





   
    date_widget.configure(text=f"{greeting} {hostname}. It is currently {formatted_time}")
    app.after(500, update_label)


# App content


    # Tabs
tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=10, pady=10)


home_tab = tabview.add("Home")
news_tab = tabview.add("News")
chat_tab = tabview.add("Chat")
settings_tab = tabview.add("Settings")


# Home content
date_widget = ctk.CTkLabel(home_tab, font=("Times New Roman", 28))
date_widget.grid(padx=0, pady=50)

song_widget = ctk.CTkLabel(home_tab, text="Be patient! Perfection takes time.", font=("Helvetica", 14))
song_widget.grid(padx=0, pady=0)



    # News content



    # Chat content
chat_frame = ctk.CTkFrame(chat_tab, width=580, height=260)
chat_frame.grid(row=0, column=0, padx=20, pady=20)


chat_display = ctk.CTkTextbox(chat_frame, width=500, height=200, font=("Helvetica", 14))
chat_display.grid(row=0, column=0, padx=0, pady=0)


chat_display.configure(state=tk.DISABLED)  # Disable editing


chat_input = ctk.CTkEntry(chat_tab, placeholder_text="Talk to Ivy...", width=480)
chat_input.grid(row=2, column=0, padx=20, pady=0)


send_btn = ctk.CTkButton(chat_tab, text="Send", width=40, command=send)
send_btn.grid(row=2, column=1, padx=10, pady=130)


        # Bind the Return key to the send function
chat_input.bind('<Return>', lambda event: send())  # Pass the function reference without parentheses


    # Settings content
        # Switching appearance mode
current_mode = 3  # 1: light, 2: dark, 3: system
print(f"System mode on startup: {current_mode}")

def dark_mode_switch():
    global current_mode
    current_mode += 1
    if current_mode > 3:
        current_mode = 1  # Reset to light mode after system mode

    if current_mode == 1:
        ctk.set_appearance_mode('light')
        print("gui.py: appearance mode changed to light mode!")
    elif current_mode == 2:
        ctk.set_appearance_mode('dark')
        print("gui.py: appearance mode changed to dark mode!")
    elif current_mode == 3:
        ctk.set_appearance_mode('system')
        print("gui.py: appearance mode changed to system mode!")

info_visible = False
info_tab = None

# Info Content (The function is declared early to I have to have the function declared before the button)

def show_info_content():
    global ip_addr_lbl
    ip_addr_lbl = ctk.CTkLabel(info_tab, text=hostname, font=("Helvetica", 14))
    ip_addr_lbl.grid(row = 0, column = 0, padx=0, pady=0)

def hide_info_content():
    ip_addr_lbl.grid_forget()

def show_info_tab():
    global info_visible, info_tab
    # Toggle visibility
    try:
        if not info_visible:
            info_tab = tabview.add("System Info")
            system_mode_on = True
            show_info_content()
            print("gui.py: System information displayed!")
        else:
            hide_info_content()
            tabview.delete(info_tab)
            system_mode_on = False
            print("gui.py: System information hidden!")
    except Exception as e:
        show_alert("Error", f"An error occurred: {e}")
        print("Error in gui.py: ", e)

if system_mode_on == True:
    show_info_tab()


settings_lbl = ctk.CTkLabel(settings_tab, text="Design and appearances", font=("Helvetica", 14))
settings_lbl.grid(row = 0, column = 0, padx=0, pady=0)


appearance_lbl = ctk.CTkLabel(settings_tab, text="Change appearance mode: ", font=("Helvetica", 14))
appearance_btn = ctk.CTkButton(settings_tab, text="Change appearance mode", command=dark_mode_switch)
appearance_lbl.grid(row = 1, column = 0, padx=0, pady=0)
appearance_btn.grid(row = 1, column = 1, padx=0, pady=0)

show_info_lbl = ctk.CTkLabel(settings_tab, text="Show system information: ", font=("Helvetica", 14))
show_info_btn = ctk.CTkButton(settings_tab, text="Show system information", command=show_info_tab)
show_info_lbl.grid(row = 2, column = 0, padx=0, pady=0)
show_info_btn.grid(row = 2, column = 1, padx=0, pady=0)

    # Info Content


update_label()
while True:
    app.mainloop()
    app.after(500, None) #I don't know what to put here
