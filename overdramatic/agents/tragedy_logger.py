from datetime import datetime

TRAGEDY_LOG_FILE = "tragedy_log.txt"

def log_tragedy(emotion, user_input):
    intense_emotions = ["hopeless", "overwhelmed", "angry", "sad"]
    if emotion in intense_emotions:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n[{timestamp}]\nEmotion: {emotion}\nUser said: {user_input}\n{'-'*60}\n"
        with open(TRAGEDY_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
