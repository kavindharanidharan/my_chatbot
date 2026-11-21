import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
if not api_key:
    raise RuntimeError("Set GROQ_API_KEY or api_key in your environment or .env file.")
client = Groq(api_key=api_key)
messages = []

print("Chatbot ready machi! Velila poga 'exit' nu type pannu.\n")

while True:
    user_input = input("Nee: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Seri machi, bye!")
        break

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(

model="openai/gpt-oss-120b",
        messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print(f"\nBot: {reply}\n")