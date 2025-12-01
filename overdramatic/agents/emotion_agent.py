from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_emotion(user_input):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        prompt = f"What is the emotional tone of this message? Respond with one word (e.g., sad, anxious, angry, confused, hopeful):\n\n\"{user_input}\""
        response = model.generate_content(prompt)
        return response.text.strip().lower()
    except Exception as e:
        return "neutral"
