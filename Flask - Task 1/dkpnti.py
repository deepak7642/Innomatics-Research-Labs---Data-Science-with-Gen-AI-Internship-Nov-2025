from flask import Flask, request
import datetime

app = Flask(__name__)


# ---------- CORE LOGIC (same as before) ----------

def mood_based_greeting(name):
    if len(name) <= 4:
        return "Short & sweet name 😎"
    elif len(name) <= 8:
        return "Perfectly balanced name ⚖️"
    else:
        return "Wow! That's a legendary name 🐉"


def name_score(name):
    score = sum(ord(char.lower()) - 96 for char in name if char.isalpha())
    return score % 100 or 50


def emoji_intelligence(name):
    if len(name) < 5:
        return "⚡"
    elif len(name) < 8:
        return "🔥"
    else:
        return "🌟"


def daily_fortune(name):
    fortunes = [
        "Today is a great day to start something new ✨",
        "An unexpected opportunity is coming 🚪",
        "Focus on learning — it will pay off 📘",
        "A small win today will boost your confidence 🏆",
        "Take a break — clarity follows rest ☕"
    ]

    today_seed = datetime.date.today().day
    index = (len(name) + today_seed) % len(fortunes)
    return fortunes[index]


def name_rarity(name):
    if len(name) <= 4:
        return "Ultra Rare 💎"
    elif len(name) <= 7:
        return "Rare 🔥"
    else:
        return "Legendary 🌟"


def vibe_meter(score):
    if score > 80:
        return "High Energy ⚡"
    elif score > 50:
        return "Chill & Balanced 🌿"
    else:
        return "Calm & Thoughtful 🌙"


def process_name(name):
    score = name_score(name)
    return {
        "name": name.upper(),
        "emoji": emoji_intelligence(name),
        "mood": mood_based_greeting(name),
        "score": score,
        "rarity": name_rarity(name),
        "vibe": vibe_meter(score),
        "fortune": daily_fortune(name)
    }


# ---------- FLASK ROUTE ----------

@app.route("/")
def home():
    name = request.args.get("name")

    if not name:
        return """
        <h2>❌ Name not provided</h2>
        <p>Try this:</p>
        <code>?name=yourname</code>
        """

    result = process_name(name)

    return f"""
    <h1>👤 Name Intelligence Report</h1>
    <h2>{result['name']} {result['emoji']}</h2>

    <p><b>🎭 Mood:</b> {result['mood']}</p>
    <p><b>🎮 Score:</b> {result['score']}/100</p>
    <p><b>🏷️ Rarity:</b> {result['rarity']}</p>
    <p><b>🎚️ Vibe:</b> {result['vibe']}</p>
    <p><b>🔮 Fortune:</b> {result['fortune']}</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
