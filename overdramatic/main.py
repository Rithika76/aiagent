from agents.advice_agent import generate_dramatic_advice
from agents.translator_agent import translate_advice
from agents.emotion_agent import detect_emotion
from agents.tragedy_logger import log_tragedy
from agents.mood_loop_agent import detect_mood_loops
from datetime import datetime
from collections import Counter

MOOD_LOG_FILE = "mood_log.txt"

def narrate_chart(title, caption):
    prompt = f"Imagine you're a poetic museum guide. Narrate this emotional chart titled '{title}' with the following caption:\n{caption}\nMake it dramatic, soulful, and under 100 words."
    narration = generate_dramatic_advice(prompt)
    print("\n🎙️ Narration:\n")
    print(narration)
def sort_chart_archive(order="newest"):
    try:
        with open("chart_archive.txt", "r", encoding="utf-8") as f:
            entries = f.read().split("="*60)
    except FileNotFoundError:
        print("\n⚠️ No chart archive found yet.")
        return

    def extract_timestamp(entry):
        for line in entry.splitlines():
            if line.startswith("["):
                try:
                    return datetime.strptime(line[1:20], "%Y-%m-%d %H:%M:%S")
                except:
                    return datetime.min
        return datetime.min

    sorted_entries = sorted(entries, key=extract_timestamp, reverse=(order == "newest"))

    print(f"\n🖼️ Chart Archive ({'Newest' if order == 'newest' else 'Oldest'} First):\n")
    for entry in sorted_entries:
        print(entry.strip())
        print("="*60)
def filter_chart_archive_by_emotion(emotion_keyword):
    try:
        with open("chart_archive.txt", "r", encoding="utf-8") as f:
            entries = f.read().split("="*60)
    except FileNotFoundError:
        print("\n⚠️ No chart archive found yet.")
        return

    matches = [entry.strip() for entry in entries if emotion_keyword.lower() in entry.lower()]
    if not matches:
        print(f"\n🔍 No charts found with emotion: '{emotion_keyword}'")
        return

    print(f"\n🎨 Charts containing '{emotion_keyword}':\n")
    for match in matches:
        print(match)
        print("="*60)
def visualize_mood_loops():
    try:
        with open(MOOD_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("\n⚠️ No mood log found. Try reflecting a few times first.")
        return

    from datetime import datetime, timedelta
    from collections import Counter
    from matplotlib import pyplot as plt

    recent_emotions = []
    cutoff = datetime.now() - timedelta(days=7)

    for i in range(len(lines)):
        if lines[i].startswith("["):
            timestamp = datetime.strptime(lines[i][1:20], "%Y-%m-%d %H:%M:%S")
            if timestamp >= cutoff:
                for j in range(i + 1, i + 4):
                    if j < len(lines) and lines[j].startswith("Emotion:"):
                        recent_emotions.append(lines[j].split(":")[1].strip())

    if not recent_emotions:
        print("\n⚠️ No recent emotions to visualize.")
        return

    counts = Counter(recent_emotions)
    emotions = list(counts.keys())
    frequencies = list(counts.values())

    # Generate poetic chart title
    summary = ", ".join([f"{emotion} ({count})" for emotion, count in counts.items()])
    title_prompt = f"Give this emotional chart a poetic title based on these emotions: {summary}. Keep it under 8 words."
    chart_title = generate_dramatic_advice(title_prompt).strip()

    # Plot chart with poetic title
    plt.figure(figsize=(10, 5))
    plt.bar(emotions, frequencies, color='teal')
    plt.title(f"📊 {chart_title}", fontsize=14)
    plt.xlabel("Emotion")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    # Generate poetic caption
    caption_prompt = f"Write a poetic caption for this emotional chart: {summary}"
    caption = generate_dramatic_advice(caption_prompt)

    print(f"\n📖 Chart Title: {chart_title}")
    print("\n🪶 Poetic Caption:\n")
    print(caption)
    log_chart(chart_title, caption)
def log_chart(title, caption):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}]\n📊 Chart Title: {title}\n🪶 Caption:\n{caption}\n{'='*60}\n"
    with open("chart_archive.txt", "a", encoding="utf-8") as f:
        f.write(entry)
def view_loop_archive():
    try:
        with open("loop_reflections.txt", "r", encoding="utf-8") as f:
            print("\n🔁 Your Loop Reflection Archive:\n")
            print(f.read())
    except FileNotFoundError:
        print("\n⚠️ No loop reflections found yet. Try reflecting on a recurring emotion first.")

def log_loop_reflection(emotion, reflection):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}]\n🔁 Looping Emotion: {emotion}\nReflection:\n{reflection}\n{'-'*60}\n"
    with open("loop_reflections.txt", "a", encoding="utf-8") as f:
        f.write(entry)

def log_mood(emotion, user_input):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}]\nEmotion: {emotion}\nUser said: {user_input}\n{'-'*60}\n"
    with open(MOOD_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def daily_reflection(reflection=None):
    if not reflection:
        return "🌅 A moment of reflection, if you will.\n\n(But no reflection was received.)"

    emotion = detect_emotion(reflection)
    log_mood(emotion, reflection)
    log_tragedy(emotion, reflection)

    response = f"🌅 A moment of reflection, if you will.\n\n🪞 You seem to be feeling {emotion}."

    looping_emotion = detect_mood_loops()
    if looping_emotion:
        response += f"\n\n🔁 I've noticed you've been feeling {looping_emotion} quite often lately."
        advice = generate_dramatic_advice(f"I've been feeling {looping_emotion} a lot lately.")
        log_loop_reflection(looping_emotion, advice)
        response += f"\n\n🌀 Loop-Breaking Reflection:\n{advice}"
    else:
        advice = generate_dramatic_advice(reflection)
        response += f"\n\n🎭 Reflective Advice:\n{advice}"

    return response

def generate_weekly_chapter_title(emotion_counts):
    summary = ", ".join([f"{emotion} ({count})" for emotion, count in emotion_counts.items()])
    prompt = f"Based on these emotions from the past week: {summary}, generate a poetic chapter title for this emotional journey. Keep it under 10 words."
    title = generate_dramatic_advice(prompt)
    return title.strip()

def log_chapter(title, reflection):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}]\n📖 {title}\n{reflection}\n{'='*60}\n"
    with open("chapter_archive.txt", "a", encoding="utf-8") as f:
        f.write(entry)

def weekly_emotional_summary():
    print("\n📜 Gathering your emotional echoes from the past week...")

    try:
        with open(MOOD_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("\n⚠️ No mood log found. Try reflecting a few times first.")
        return

    emotions = [line.strip().split(":")[1].strip() for line in lines if line.startswith("Emotion:")]
    if not emotions:
        print("\n⚠️ No emotions recorded yet.")
        return

    emotion_counts = Counter(emotions)
    summary = ", ".join([f"{emotion} ({count})" for emotion, count in emotion_counts.items()])
    title = generate_weekly_chapter_title(emotion_counts)
    prompt = f"Write a poetic reflection on a week filled with these emotions: {summary}"
    reflection = generate_dramatic_advice(prompt)

    print(f"\n📖 Chapter Title: {title}")
    print("\n🪶 Weekly Emotional Reflection:\n")
    print(reflection)

    log_chapter(title, reflection)

def view_chapter_archive():
    try:
        with open("chapter_archive.txt", "r", encoding="utf-8") as f:
            print("\n📚 Your Chapter Archive:\n")
            print(f.read())
    except FileNotFoundError:
        print("\n⚠️ No archive found yet. Try generating a weekly summary first.")

def main():
    last_advice = None

    print("\n🎭 Welcome, dear soul. Let us begin.")

    while True:
        user_input = input("\nWhat weighs upon thy heart today?\n(Or type 'reflect', 'summary', 'archive', 'loops', 'loopchart', 'charts', 'charts with [emotion]', 'charts newest', 'charts oldest', or 'exit')\n> ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nFare thee well. May your story unfold with grace.")
            break

        elif user_input.lower() == "reflect":
            daily_reflection()
            continue

        elif user_input.lower() == "summary":
            weekly_emotional_summary()
            continue

        elif user_input.lower() == "archive":
            view_chapter_archive()
            continue
        elif user_input.lower() == "loops":
            view_loop_archive()
            continue
        elif user_input.lower() == "loopchart":
            visualize_mood_loops()
            continue
        elif user_input.lower().startswith("charts with "):
            emotion_keyword = user_input[12:].strip()
            filter_chart_archive_by_emotion(emotion_keyword)
            continue
        elif user_input.lower() == "charts newest":
             sort_chart_archive(order="newest")
            continue

        elif user_input.lower() == "charts oldest":
             sort_chart_archive(order="oldest")
             continue

        last_advice = generate_dramatic_advice(user_input)
        print("\n🎭 Dramatic Advice:\n")
        print(last_advice)

        emotion = detect_emotion(user_input)
        log_mood(emotion, user_input)
        log_tragedy(emotion, user_input)

        # 🔁 Mood loop detection
        looping_emotion = detect_mood_loops()
        if looping_emotion:
            print(f"\n🔁 I've noticed you've been feeling {looping_emotion} quite often lately.")
            loop_check = input("Would you like to reflect on that a little more? (yes/no)\n> ").strip().lower()
            if loop_check == "yes":
                advice = generate_dramatic_advice(f"I've been feeling {looping_emotion} a lot lately.")
                print("\n🌀 Loop-Breaking Reflection:\n")
                print(advice)

        style_map = {
            "sad": "motivational coach",
            "anxious": "emoji-only wisdom",
            "angry": "pirate speak",
            "confused": "Gen Z slang",
            "hopeless": "motivational coach",
            "overwhelmed": "emoji-only wisdom"
        }

        style = style_map.get(emotion, None)

        if style:
            suggestion = input(f"\nYou seem a bit {emotion}. Would you like me to rephrase that in {style}? (yes/no)\n> ").strip().lower()
            if suggestion == "yes":
                translated = translate_advice(last_advice, style)
                print(f"\n🌀 Translated Advice ({style}):\n")
                print(translated)
            else:
                print("\nNo worries. The original wisdom shall stand.")
        else:
            print("\nAs you wish. Let the words settle in thy soul.")

if __name__ == "__main__":
    main()

