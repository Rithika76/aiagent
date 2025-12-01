from dotenv import load_dotenv
import os
import google.generativeai as genai
from datetime import datetime

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

LOG_FILE = "advice_log.txt"

def log_advice(user_input, response_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[{timestamp}]\nUser: {user_input}\nAdvice:\n{response_text}\n{'-'*60}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def generate_dramatic_advice(user_input):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        prompt = f"Respond like Shakespeare giving life advice to someone who says: '{user_input}'"
        response = model.generate_content(prompt)
        advice = response.text.strip()
        log_advice(user_input, advice)
        return advice
    except Exception as e:
        return "Gemini failed to respond."
