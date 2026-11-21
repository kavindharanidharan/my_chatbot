from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
if not api_key:
    raise RuntimeError("Set GROQ_API_KEY or api_key in your environment or .env file.")
client = Groq(api_key=api_key)

SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful and friendly AI assistant for TechNova mini project."}
chat_history = [SYSTEM_PROMPT]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/clear", methods=["POST"])
def clear():
    chat_history.clear()
    chat_history.append(SYSTEM_PROMPT)
    return jsonify({"status": "cleared"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        chat_history.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=chat_history)
        bot_reply = response.choices.__getitem__(0).message.content
        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
