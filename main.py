import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import colorama as clr
import os
import json
import datetime

counter = 0

def run_counter():
    global counter
    counter += 1
    save_counter(counter)
    print(f"Runs: {counter}")

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

chat_history_file = "chat_history.json"

def load_counter():
    try:
        with open('counter.txt', 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_counter(counter):
    try:
        with open('counter.txt', 'w') as file:
            file.write(str(counter))
    except Exception as e:
        print(f"Error saving counter: {e}")

def load_history():
    try:
        with open(chat_history_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error 55")

def save_history(history):
    try:
        with open(chat_history_file, 'w') as file:
            json.dump(history, file)
    except Exception as e:
        print(f"{clr.Fore.RED}Error 62: {e}", end='')

try:
    with open(chat_history_file, 'r') as file:
        history = json.load(file)
except FileNotFoundError:
    history = [
        {"role": "model", "parts": "Hello, Charles. I am your personal assistant."},
        {"role": "user", "parts": "Hello, Ivy"}
    ]

# Start chat with the loaded history
chat = model.start_chat(history=history)

def callback_mode(): #Made for 1 input, more resembling google assistant
    pass


def conversation_mode():
    print("Welcome back, Charles. Type /help for details")
    while True:
        user_input = input(f"{clr.Fore.WHITE}You: ")
        user_input = user_input.lower()

        if "/end" in user_input:
            print("Goodbye!")
            os.system('cls')
            break

        elif "/reset" in user_input:
            os.system('cls')
            conversation_mode()  # talk() again to reset the conversation
            break  # This break is not necessary since talk() will start a new loop
        
        elif "/help" in user_input:
            print("/end - End conversation \n/reset - Reset conversation to last recorded message \n")
            conversation_mode()
            break 

        elif "what" and "time" in user_input:
            print(datetime.time())

        else:
            try:
                response = chat.send_message(user_input)
                try:
                    user_interaction = {"role": "user", "parts":f"{user_input}"}

                    history.append(user_interaction)
                except:
                    pass

                print(f"{clr.Fore.GREEN}Ivy: {response.text}", end='')

                try:
                
                    model_interaction = {"role": "model", "parts": f"{response.text}"}

                    history.append(model_interaction)
                    save_history(history)
                    

                except:
                    pass


                if "speak" in user_input:
                    while True:
                        return response.text
            except Exception as e:
                print(f"{clr.Fore.RED}Error: {e}")



if __name__ == "__main__":
    run_counter()
    conversation_mode()