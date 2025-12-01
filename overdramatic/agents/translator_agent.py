from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def translate_advice(original_text, style):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
        prompt = f"Rewrite the following Shakespearean advice in {style} style:\n\n{original_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Translation failed: {e}"
