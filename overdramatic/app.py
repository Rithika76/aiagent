from flask import Flask, request, jsonify, render_template
from main import daily_reflection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reflect", methods=["POST"])
def reflect():
    user_input = request.json.get("text")
    if not user_input:
        return jsonify({"response": "No reflection received."})
    response = daily_reflection(user_input)
    return jsonify({"response": response})
