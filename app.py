from flask import Flask, request, render_template, Markup
import markdown2
import os
from config import configure_ai  # Import the AI model configuration
import google.generativeai as genai
import requests

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-123')  # Update this

# Initialize AI model
model = configure_ai()

# Telegram Bot Setup
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
    explanation = model.generate_content(f"Explain {doubt} in simple terms with examples").text

    # Generate practice questions
    questions = model.generate_content(f"Generate 3 practice questions about {doubt} with answers").text

    response = f"*Explanation*:\n{explanation}\n\n*Practice Questions*:\n{questions}"
    send_message(chat_id, response)

def setup_telegram_webhook(app):
    @app.route('/telegram-webhook', methods=['POST'])
    def telegram_webhook():
        update = request.json
        if 'message' in update:
            Thread(target=process_telegram_message, args=(update['message'],)).start()
        return '', 200

    # Set webhook URL
    webhook_url = f"{os.environ['RENDER_EXTERNAL_URL']}/telegram-webhook"
    requests.get(f"{BASE_URL}/setWebhook?url={webhook_url}")

# Call to set up the Telegram webhook after the AI model is initialized
setup_telegram_webhook(app)

# Markdown filter for rendering
@app.template_filter('markdown')
def markdown_filter(text):
    return Markup(markdown2.markdown(text))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolve_doubt', methods=['POST'])
def resolve_doubt():
    doubt = request.form['doubt']

    # Generate explanation
    explanation = model.generate_content(f"Explain {doubt} in simple terms with examples").text

    # Generate practice questions
    questions = model.generate_content(f"Generate 3 practice questions about {doubt} with answers").text

    return render_template('index.html',
                         response=explanation,
                         practice_questions=questions)

# Render Deployment Setup (web server)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Change port if necessary for Render deployment
