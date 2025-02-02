from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')

# Validate API key on startup
if not os.getenv('GEMINI_API_KEY'):
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.json
    topic = data.get('topic', '')
    
    prompt = f"Generate 5 practice questions about {topic} for competitive exam students. Include varying difficulty levels."
    
    try:
        response = model.generate_content(prompt)
        return jsonify({
            'questions': response.text.split('\n')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask_doubt', methods=['POST'])
def ask_doubt():
    data = request.json
    question = data.get('question', '')
    
    prompt = f"Explain this concept in simple terms and provide examples: {question}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({
            'explanation': response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
