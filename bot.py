import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# Start a chat session (optional, useful for context history)
chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["You are a helpful assistant."]
    },
    {
        "role": "model",
        "parts": ["Understood. I'm here to help!"]
    }
])

def get_gpt_response(prompt):
    try:
        # Get response from Gemini chat
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
user_input = "What is the capital of France?"
bot_reply = get_gpt_response(user_input)
print("Bot Response:", bot_reply)
