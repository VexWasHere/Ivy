import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

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

chat = model.start_chat(
    history = [
        {"role": "user", "parts": "Hey Ivy. I'm working on making a new project!"},
        {"role": "model", "parts": "Sounds great! What's it about?"}
    ]
)

print("Welcome back, Charles. Type /end to quit")
engine.say("Welcome back, Charles!")

while True:
    with sr.Microphone() as source:
        print("Please say something.")
        #recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio_data = recognizer.listen(source, timeout=5)  # Set a timeout for listening
            print("Listening...")
            text = recognizer.recognize_google(audio_data)
            print(f"You: {text}")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
            continue  # Go back to the start of the loop to listen again
        except sr.RequestError:
            print("Could not request results; this could be from your network being offline.")
            user_input = input("You: ")
            user_input = user_input.lower()
            if "/end" in user_input:
                print("Goodbye!")
                break
            else:
                try:
                    response = chat.send_message(user_input)
                    print(f"Ivy: {response.text}")
                    engine.say(response.text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"An error occurred: {e}")
            continue  # Go back to the start of the loop

        # Process the recognized text
        user_input = text.lower()
        if "/end" in user_input:
            print("Goodbye!")
            break
        else:
            try:
                response = chat.send_message(user_input)
                print(f"Ivy: {response.text}")
                engine.say(response.text)
                engine.runAndWait()
            except Exception as e:
                print(f"An error occurred: {e}")