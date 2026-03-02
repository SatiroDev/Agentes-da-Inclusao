# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("AIzaSyDk1QufuB6HTyQlyAP6Nu3dsrEgu8HRey8"))

# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Diga olá em português")

# print(response.text)

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY:", os.getenv("GOOGLE_API_KEY"))

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

