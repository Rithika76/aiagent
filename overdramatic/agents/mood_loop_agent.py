from collections import Counter
from datetime import datetime, timedelta

MOOD_LOG_FILE = "mood_log.txt"

def detect_mood_loops(days=7, threshold=3):
    try:
        with open(MOOD_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None  # No log to analyze

    recent_emotions = []
    cutoff = datetime.now() - timedelta(days=days)

    for i in range(len(lines)):
        if lines[i].startswith("["):
            timestamp = datetime.strptime(lines[i][1:20], "%Y-%m-%d %H:%M:%S")
            if timestamp >= cutoff:
                for j in range(i+1, i+4):
                    if j < len(lines) and lines[j].startswith("Emotion:"):
                        recent_emotions.append(lines[j].split(":")[1].strip())

    if not recent_emotions:
        return None

    counts = Counter(recent_emotions)
    most_common = counts.most_common(1)[0]
    if most_common[1] >= threshold:
        return most_common[0]  # Return the looping emotion
    return None
