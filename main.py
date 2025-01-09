import platform
import tkinter as tk
from tkinter import *
import customtkinter as ctk
import speech_recognition as sr
from win11toast import toast

def speak():
    r = sr.Recognizer()
    print("Active!")

    with sr.Microphone(1) as source:
        audio_data = r.record(source, duration=10)
        print("Processing...")
        text = r.recognize_google(audio_data)
        print(text)

def check_windows_version():
    os_version = platform.version()
    major_version = platform.version().split('.')[0]
    build_number = int(platform.version().split('.')[2])

    if major_version == "10":
        if build_number >= 22000:
            return "Windows 11"
        else:
            return "Windows 10"
    else:
        return "Not Windows 10 or 11"

def send_notif():
    windows_version = check_windows_version()
    if "Not Windows 10 or 11" in windows_version:
        print("Not Windows 10 or 11")
    elif "11" in windows_version:
        print("Windows 11")
    elif "10" in windows_version:
        print("Windows 10")

def main():
    send_notif()
    app = ctk.CTk()
    app.title("Speech Recognition")
    app.geometry("300x200")
    label = ctk.CTkLabel(app, text="Speech Recognition")

    label.pack()
    app.mainloop()

if __name__ == '__main__':
    main()