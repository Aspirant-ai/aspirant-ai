# app.py - Add these changes
from flask import Flask, request, render_template, Markup
import google.generativeai as genai
import os
import markdown2

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-123')  # Update this

# Configure Generative AI
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Markdown filter
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
    questions = model.generate_content(
        f"Generate 3 practice questions about {doubt} with answers").text
    
    return render_template('index.html',
                         response=explanation,
                         practice_questions=questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)