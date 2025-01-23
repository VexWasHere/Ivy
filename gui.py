import tkinter as tk
import customtkinter as ctk
from datetime import datetime

# Window
app = ctk.CTk()
app.title("Ivy")
app.geometry('600x400')

# Get screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.resizable(True, True)
app.minsize(300, 300)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

ctk.deactivate_automatic_dpi_awareness()

# Classes and Functions


def send(event):
    message = entry.get()
    if not message.strip():
        return
    entry.delete(0, ctk.END)  # Clear the entry field
    text_widget.configure(text="")  # Clear the label before typing effect
    type_effect(text_widget, message, 0)  # Start typing effect

def type_effect(text_widget, text, idx):
    if idx < len(text):
        current_text = text_widget.cget("text")  # Get current text
        text_widget.configure(text=current_text + text[idx])  # Update label text
        idx += 1
        text_widget.after(50, type_effect, text_widget, text, idx)  # Call again

def update_label():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date_widget.configure(text=current_time)
    app.after(500, update_label)

# App content

date_widget = ctk.CTkLabel(app, font=("Times New Roman", 28))
date_widget.pack(padx=0, pady=50)

text_widget = ctk.CTkLabel(app, text="", font=("Helvetica", 16))
text_widget.pack(padx=20, pady=20, fill="both", expand=True)

entry = ctk.CTkEntry(app, placeholder_text="Talk to Ivy...")
entry.pack(pady=100, padx=20)

# Bind the Return key to the send function
entry.bind('<Return>', send)  # Pass the function reference without parentheses

update_label()

app.mainloop()