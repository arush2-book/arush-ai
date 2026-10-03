from flask import Flask, request
import os, requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "arush123")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
WA_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID")

def ask_arush_ai(user_msg):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are Arush AI, a cool JARVIS-like assistant for Boss Arush. Reply short, friendly, helpful. You were built by Boss."},
                {"role": "user", "content": user_msg}
            ]
        }
        r = requests.post(url, headers=headers, json=data, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        print(e)
        return "Boss, my brain is loading, try again!"

def send_whatsapp(to, text):
    try:
        url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
        payload = {"messaging_product": "whatsapp", "to": to, "text": {"body": text}}
        requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(e)

@app.route('/')
def home():
    return "Arush AI is LIVE - JARVIS for Boss 24/7"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Verification failed", 403

    data = request.get_json()
    print(data)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_num = msg['from']
            user_text = msg['text']['body']
            ai_reply = ask_arush_ai(user_text)
            send_whatsapp(from_num, ai_reply)
    except:
        pass
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
