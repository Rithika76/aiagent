from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_dramatic_advice(user_input):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        prompt = f"Respond like Shakespeare giving life advice to someone who says: '{user_input}'"
        print("📨 Sending prompt to Gemini:", prompt)
        response = model.generate_content(prompt)
        print("✅ Gemini raw response:", response)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini error:", e)
        return "Gemini failed to respond."
