from tkinter import *
import customtkinter as ctk
from datetime import datetime
import socket
from google import genai
import textwrap
from PIL import Image
import speech_recognition as sr
import threading   # NEW

r = sr.Recognizer()

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
    if hour == 0:
        hour = 12

current_time = f"{hour}:{minute:02d} {hour_suffix}"

# --- App setup ---
app = ctk.CTk()
app.title("Ivy test")
app.geometry("600x400")
app.iconbitmap('snakeimg.ico')
app.resizable(False, False)

ctk.deactivate_automatic_dpi_awareness()
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

terminal_name = socket.gethostname()

# --- Shared font object ---
app_font = ctk.CTkFont(size=20)

# --- Globals ---
chat = None
chat_frame = None
mic_names = []
selected_mic_index = 0   # ✅ define globally here

# --- Functions ---
def wrap_text(text, limit=45):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
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
        system_prompt = (
            "You are Ivy, a friendly and knowledgeable AI assistant. "
            "Your purpose is to help the user with clear, concise, and engaging answers. "
            "Always respond in a warm, approachable tone while also keeping it short and sweet."
            f"User: {msg}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[system_prompt]
        ).text
        response = wrap_text(response, limit=45)

        print(f"{terminal_name}: {msg}")
        ctk.CTkLabel(chat_frame, text=f"{terminal_name}: {msg}",
                     font=app_font, anchor="w").pack(pady=0, anchor="w")
        ctk.CTkLabel(chat_frame, text=f"\nIvy: {response}\n",
                     font=app_font, anchor="w").pack(pady=0, anchor="w")
        chat.delete(0, 'end')

def change_appearance_mode(new_mode):
    ctk.set_appearance_mode(new_mode)

def set_font_size(size_label):
    sizes = {"Small": 12, "Medium": 20, "Large": 28}
    new_size = sizes.get(size_label, 20)
    app_font.configure(size=new_size)
    print(f"Font size changed to {size_label} ({new_size})")

def listen_microphone():
    def _worker():
        global selected_mic_index
        try:
            with sr.Microphone(device_index=selected_mic_index) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print(f"🎤 Listening on mic index {selected_mic_index}...")
                audio_txt = r.listen(source, phrase_time_limit=8)
                text = r.recognize_google(audio_txt)
                print("You said:", text)
                chat.after(0, lambda: chat.insert(0, text))
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected.")
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError as e:
            print(f"⚠️ API error: {e}")
    threading.Thread(target=_worker, daemon=True).start()

def set_microphone(choice):
    global selected_mic_index
    selected_mic_index = mic_names.index(choice)
    print(f"🎙️ Microphone set to: {choice} (index {selected_mic_index})")

# --- Main UI ---
def main():
    global chat, chat_frame, mic_names, selected_mic_index

    tabview = ctk.CTkTabview(app)
    tabview.pack(fill=BOTH, expand=True)

    # HOME
    home_tab = tabview.add("Home")
    ctk.CTkLabel(home_tab, text=f"Hello, {terminal_name}!", font=app_font).pack(pady=20)
    ctk.CTkLabel(home_tab, text=f"The time is {current_time}", font=app_font).pack(pady=10)

    # CHAT
    chat_tab = tabview.add("Chat")
    chat_frame = ctk.CTkScrollableFrame(chat_tab, width=200, height=200)
    chat_frame.pack(pady=20, padx=20, fill="both", expand=True)

    entry_frame = ctk.CTkFrame(chat_tab)
    entry_frame.pack(fill="x", pady=10, padx=20)

    chat = ctk.CTkEntry(entry_frame, placeholder_text="Type your message here...", width=300, font=app_font)
    chat.pack(side="left", padx=(0, 10))
    chat.bind("<Return>", send)

    light_icon = Image.open("mic_black.png").resize((24, 24))
    dark_icon = Image.open("mic_white.png").resize((24, 24))
    mic_img = ctk.CTkImage(light_image=light_icon, dark_image=dark_icon, size=(24, 24))

    ctk.CTkButton(entry_frame, image=mic_img, text="", width=40,
                  command=listen_microphone).pack(side="left", padx=(0, 10))

    ctk.CTkButton(entry_frame, text="Send", width=100, command=send, font=app_font).pack(side="left")

    # SETTINGS
    settings_tab = tabview.add("Settings")
    ctk.CTkLabel(settings_tab, text="Settings", font=app_font).pack(pady=20)
    settings_scrollframe = ctk.CTkScrollableFrame(settings_tab, width=200, height=200)
    settings_scrollframe.pack(pady=10, padx=10, fill="both", expand=True)

    ctk.CTkLabel(settings_scrollframe, text="Appearance Mode:", font=app_font).pack(pady=10, padx=10, anchor='w')
    appearance_mode = ctk.CTkOptionMenu(settings_scrollframe,
                                        values=["Light", "Dark", "System"],
                                        command=change_appearance_mode,
                                        font=app_font)
    appearance_mode.pack(pady=10, padx=10, anchor='w')

    ctk.CTkLabel(settings_scrollframe, text="Font Size:", font=app_font).pack(pady=10, padx=10, anchor='w')
    font_size = ctk.CTkOptionMenu(settings_scrollframe,
                                  values=["Small", "Medium", "Large"],
                                  command=set_font_size,
                                  font=app_font)
    font_size.pack(pady=10, padx=10, anchor='w')

    mic_names = sr.Microphone.list_microphone_names()

    mic_label = ctk.CTkLabel(settings_scrollframe, text="Microphone:", font=app_font)
    mic_label.pack(pady=10, padx=10, anchor='w')

    mic_menu = ctk.CTkOptionMenu(settings_scrollframe,
                                values=mic_names,
                                command=set_microphone,
                                font=app_font)
    mic_menu.pack(pady=10, padx=10, anchor='w')

    # Default to system default mic
    selected_mic_index = 0
    mic_menu.set(mic_names[0])

    appearance_mode.set("Dark")
    font_size.set("Medium")

    tabview.set("Home")
    app.mainloop()

if __name__ == "__main__":
    print("Starting system...")
    main()