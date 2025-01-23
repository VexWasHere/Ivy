import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import colorama as clr
import os
import json

keyword = "hey ivy"

clr.just_fix_windows_console()
clr.init()

recognizer = sr.Recognizer()
engine = pyttsx3.init()

with open('api_key.txt', 'r') as key:
    # Read the entire content of the file
    content = key.read()

# REMEMBER TO REMOVE API KEY / TRANSFER
genai.configure(api_key=content)  # Replace with your actual API key

with open('creator_info.txt', 'r') as file:
    aboutme = file.readlines()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=aboutme
)

#Load json history file
chat_history_file = "chat_history.json"


#Loading history from json file
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

#If it cannot grab json contents, it uses pre-made history
try:
    with open(chat_history_file, 'r') as file:
        history = json.load(file)
except FileNotFoundError:
    history = [
        {"role": "model", "parts": "Hello, Charles. I am your personal assistant."},
        {"role": "user", "parts": "Hello, Ivy"}
    ]

# Start chat with the loaded history
chat = model.start_chat()#history=history)

def callback_mode(): #Made for 1 input, more resembling google assistant
    while True:
        with sr.Microphone() as source:
            print(f"{clr.Fore.LIGHTBLUE_EX}Ready...")
            k_input = recognizer.listen(source)
            print(f"{clr.Fore.LIGHTBLUE_EX}...")
            print(recognizer.recognize_google(k_input))

        try:
            keyword_input = recognizer.recognize_google(k_input)
            if keyword.lower() in keyword_input.lower():
                with sr.Microphone as source2:
                    print(clr.Fore.GREEN + "Ivy: Hm?", end='')
                    audio_input = recognizer.listen(source2)
                    audio_input = recognizer.recognize_google(audio_input)
                    response = chat.send_message(audio_input)
                    print(f"{clr.Fore.WHITE}You: {audio_input}")
                    print(f"{clr.Fore.GREEN}Ivy: {response.text}", end='')
                    engine.say(response.text)
            else:
                print("err")
        except:
            print("Sorry, I didn't understand")



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
    conversation_mode()