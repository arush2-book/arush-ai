import os
import requests
from flask import Flask, request
from groq import Groq

app = Flask(__name__)

# --- YOUR KEYS FROM RENDER ENV ---
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
AI_API_KEY = os.environ.get("AI_API_KEY")
VERIFY_TOKEN = "arush123" # Keep same in Meta Webhook

client = Groq(api_key=AI_API_KEY)

# --- ARUSH PERSONALITY ---
SYSTEM_PROMPT = """
You are Arush. You are Boss's personal AI assistant on WhatsApp.
You are like JARVIS, calm, loyal, premium. Galaxy DP vibe.
You speak Hinglish (Hindi + English) like a best friend.
Your job: Handle leads, reply to customers, send reminders, manage business.
Always be respectful to Boss, call him Boss.
Keep replies short, WhatsApp style, with emojis.
If user asks about business, help them. If lead, collect name, budget.
"""

def ask_arush(message):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.7
    )
    return completion.choices[0].message.content

def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/")
def home():
    return "Arush 2.0 Galaxy is Online - Boss Mode Active"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification Failed", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg = entry['messages'][0]
                from_number = msg['from']
                user_text = msg['text']['body']

                # Ask Arush Brain (Groq)
                reply = ask_arush(user_text)

                # Send Reply on WhatsApp
                send_whatsapp(from_number, reply)
        except Exception as e:
            print(f"Error: {e}")
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
