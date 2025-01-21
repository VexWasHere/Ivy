import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import colorama as clr
import os
import json

clr.just_fix_windows_console()
clr.init()

recognizer = sr.Recognizer()
engine = pyttsx3.init()


# REMEMBER TO REMOVE API KEY / TRANSFER
genai.configure(api_key="AIzaSyAzUb-jta-rZH9VoiWaWwz50nBJxCdvNaI")  # Replace with your actual API key


with open('creator_info.txt', 'r') as file:
    aboutme = file.readlines()


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=aboutme
)

chat_history_file = '/chat_history.json'


def load_chat_history():
    if os.path.exists(chat_history_file):
        with open(chat_history_file, 'r') as file:
            return json.load(file)
    else:
        return []

def save_chat_history(history):
    with open(chat_history_file, 'w') as file:
        json.dump(history, file, indent=4)

def add_to_chat_history(role, parts):
    history = load_chat_history()
    history.append({"role": role, "parts": parts})
    save_chat_history(history)

# Load chat history safely
try:
    data = load_chat_history()
except Exception as e:
    print(f"Error loading chat history: {e}")
    data = []

# Check if 'history' key exists in the loaded data
history = data.get('history', [])  # Use an empty list if 'history' key is not found

# Start chat with the loaded history
chat = model.start_chat(history=history)


def talk():
    print("Welcome back, Charles. Type /end to quit")
    while True:
        user_input = input(f"{clr.Fore.WHITE}You: ")
        user_input = user_input.lower()

        if "/end" in user_input:
            print("Goodbye!")
            os.system('cls')
            break

        elif "/reset" in user_input:
            os.system('cls')
            talk()  # talk() again to reset the conversation
            break  # This break is not necessary since talk() will start a new loop

        else:
            try:
                response = chat.send_message(user_input)
                print(f"{clr.Fore.GREEN}Ivy: {response.text}", end='')
                if "speak" in user_input:
                    while True:
                        return response.text
            except Exception as e:
                print(f"{clr.Fore.RED}Error: {e}")



if __name__ == "__main__":
    talk()