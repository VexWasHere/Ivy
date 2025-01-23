import tkinter as tk
import customtkinter as ctk

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

# App content


entry = ctk.CTkEntry(app, placeholder_text="Talk to Ivy...")
entry.pack(pady=100, padx=20)

app.mainloop()