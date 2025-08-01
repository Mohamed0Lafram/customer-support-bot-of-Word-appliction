from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# Access the keys
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)