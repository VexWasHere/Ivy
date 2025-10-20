from tkinter import *
import customtkinter as ctk
from datetime import datetime
import socket
from google import genai
import textwrap

client = genai.Client(api_key="AIzaSyAzUb-jta-rZH9VoiWaWwz50nBJxCdvNaI")

# --- Time formatting ---
now = datetime.now()
hour = int(now.strftime("%H"))
minute = int(now.strftime("%M"))

if hour >= 12:
    hour_suffix = "PM"
    if hour > 12:
        hour -= 12
else:
    hour_suffix = "AM"
    if hour == 0:  # midnight case
        hour = 12

current_time = f"{hour}:{minute:02d} {hour_suffix}"

# --- App setup ---
app = ctk.CTk()
app.title("Ivy 0.1")
app.geometry("600x400")
app.iconbitmap('snakeimg.ico')
app.resizable(False, False)

ctk.deactivate_automatic_dpi_awareness()
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

terminal_name = socket.gethostname()

# --- Shared font object (all widgets use this) ---
app_font = ctk.CTkFont(size=20)

# --- Globals ---
chat = None
chat_frame = None

# --- Functions ---
def wrap_text(text, limit=45):
    """
    Wrap text at spaces so words aren't cut in half.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # +1 accounts for the space
        if len(current_line) + len(word) + 1 <= limit:
            current_line += (word + " ")
        else:
            lines.append(current_line.rstrip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.rstrip())

    return "\n".join(lines)


def send(event=None):
    msg = chat.get()
    if msg != "":
        # Persona definition for Ivy
        system_prompt = (
            "You are Ivy, a friendly and knowledgeable AI assistant. "
            "Your purpose is to help the user with clear, concise, and engaging answers. "
            "Always respond in a warm, approachable tone while also keeping it short and sweet."
            f"User: {msg}"
        )

        # Call Gemini with persona + user message
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[system_prompt]
        ).text
        response = wrap_text(response, limit=45)

        # Display user + AI messages in the chat window
        print(f"{terminal_name}: {msg}")
        ctk.CTkLabel(chat_frame, text=f"{terminal_name}: {msg}",
                     font=app_font, anchor="w").pack(pady=0, anchor="w")
        ctk.CTkLabel(chat_frame, text=f"\nIvy: {response}\n",
                     font=app_font, anchor="w").pack(pady=0, anchor="w")
        chat.delete(0, 'end')

def change_appearance_mode(new_mode):
    ctk.set_appearance_mode(new_mode)

def set_font_size(size_label):
    if size_label == "Small":
        new_size = 12
    elif size_label == "Medium":
        new_size = 20
    elif size_label == "Large":
        new_size = 28
    else:
        new_size = 20
    app_font.configure(size=new_size)  # updates all widgets using app_font
    print(f"Font size changed to {size_label} ({new_size})")

# --- Main UI ---
def main():
    global chat, chat_frame

    tabview = ctk.CTkTabview(app)
    tabview.pack(fill=BOTH, expand=True)

    # HOME
    home_tab = tabview.add("Home")
    label = ctk.CTkLabel(home_tab, text=f"Hello, {terminal_name}!", font=app_font)
    label.pack(pady=20)

    time_lbl = ctk.CTkLabel(home_tab, text=f"The time is {current_time}", font=app_font)
    time_lbl.pack(pady=10)

    # CHAT
    chat_tab = tabview.add("Chat")

    chat_frame = ctk.CTkScrollableFrame(chat_tab, width=200, height=200)
    chat_frame.pack(pady=20, padx=20, fill="both", expand=True)

    chat = ctk.CTkEntry(chat_tab, placeholder_text="Type your message here...", width=400, font=app_font)
    chat.pack(anchor="s", side="left", pady=10)
    chat.bind("<Return>", send)

    chat_button = ctk.CTkButton(chat_tab, text="Send", width=150, command=send, font=app_font)
    chat_button.pack(anchor="s", side="right", pady=10, padx=20)

    # SETTINGS
    settings_tab = tabview.add("Settings")
    settings_label = ctk.CTkLabel(settings_tab, text="Settings", font=app_font)
    settings_label.pack(pady=20)

    settings_scrollframe = ctk.CTkScrollableFrame(settings_tab, width=200, height=200)
    settings_scrollframe.pack(pady=10, padx=10, fill="both", expand=True)

    appearance_mode_label = ctk.CTkLabel(settings_scrollframe, text="Appearance Mode:", font=app_font)
    appearance_mode_label.pack(pady=10, padx=10, anchor='w')

    appearance_mode = ctk.CTkOptionMenu(settings_scrollframe,
                                        values=["Light", "Dark", "System"],
                                        command=change_appearance_mode,
                                        font=app_font)
    appearance_mode.pack(pady=10, padx=10, anchor='w')

    font_size_label = ctk.CTkLabel(settings_scrollframe, text="Font Size:", font=app_font)
    font_size_label.pack(pady=10, padx=10, anchor='w')

    font_size = ctk.CTkOptionMenu(settings_scrollframe,
                                  values=["Small", "Medium", "Large"],
                                  command=set_font_size,
                                  font=app_font)
    font_size.pack(pady=10, padx=10, anchor='w')

    appearance_mode.set("Dark")
    font_size.set("Medium")

    tabview.set("Home")
    app.mainloop()

if __name__ == "__main__":
    print("Starting system...")
    main()