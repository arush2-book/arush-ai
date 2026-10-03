from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "arush123")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/')
def home():
    return "Arush AI is LIVE - JARVIS for Boss 24/7"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        return "Verification failed", 403
    
    # POST - handle WhatsApp messages
    data = request.get_json()
    print(data)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
