import google.generativeai as genai

genai.configure(api_key="AIzaSyAzUb-jta-rZH9VoiWaWwz50nBJxCdvNaI")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)