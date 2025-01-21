import google.generativeai as genai
import json

#REMEMBER TO REMOVE API KEY / TRANSFER

#Setting up AI
genai.configure(api_key="AIzaSyAzUb-jta-rZH9VoiWaWwz50nBJxCdvNaI")

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    system_instruction = "You are a personal assistant named Ivy. You give short, meaningful responses. Your goal is to support me in every way.")

chat = model.start_chat()

print("Welcome to Ivy! Type /end to quit")

while True:
    user_input = input("You: ")
    user_input = user_input.lower

    if "/end" in user_input:
        return 0
    else:
        response = chat.send_message(user_input)
        print(f"Ivy: {response.text}")


