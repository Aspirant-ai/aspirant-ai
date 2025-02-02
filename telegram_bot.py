import os
import requests
from flask import Flask
from threading import Thread
from app import model  # Reuse the existing AI model

TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def process_telegram_message(message):
    chat_id = message['chat']['id']
    doubt = message.get('text', '')
    
    # Generate explanation
    explanation = model.generate_content(
        f"Explain {doubt} in simple terms with examples").text
    
    # Generate practice questions
    questions = model.generate_content(
        f"Generate 3 practice questions about {doubt} with answers").text
    
    response = f"*Explanation*:\n{explanation}\n\n*Practice Questions*:\n{questions}"
    send_message(chat_id, response)

def setup_telegram_webhook(app):
    @app.route('/telegram-webhook', methods=['POST'])
    def telegram_webhook():
        update = request.json
        if 'message' in update:
            Thread(target=process_telegram_message, 
                 args=(update['message'],)).start()
        return '', 200

    # Set webhook URL
    webhook_url = f"{os.environ['RENDER_EXTERNAL_URL']}/telegram-webhook"
    requests.get(f"{BASE_URL}/setWebhook?url={webhook_url}")