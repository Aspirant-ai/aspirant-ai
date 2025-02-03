from flask import Flask, request, render_template, Response, stream_with_context, session, jsonify, url_for
import os
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-123')

# Validate environment variables
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_response(user_query):
    """Generates structured responses with enhanced error handling"""
    try:
        # Clean history before sending to AI model
        clean_history = [
            {'role': 'user' if msg['is_user'] else 'assistant', 'content': msg['text']}
            for msg in session.get('chat_history', [])
        ]
        
        # Create context-aware prompt
        context_prompt = f"""
        Current conversation history:
        {clean_history[-3:]}
        
        New query: {user_query}
        """
        
        response = model.generate_content(context_prompt)
        return response.text
        
    except genai.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error generating response: {str(e)}"


@app.before_request
def check_session_and_validate_context():
    # Initialize chat history if not present
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Clean old messages older than 30 minutes
    if 'chat_history' in session:
        now = datetime.now()
        session['chat_history'] = [
            msg for msg in session['chat_history'] 
            if (now - datetime.fromisoformat(msg['time'])).seconds < 1800
        ]

# Rest of the routes remain the same as in your code...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        try:
            user_query = request.args.get('q')
            full_response = generate_response(user_query)
            sentences = [s + '.' for s in full_response.split('. ') if s]
            for sentence in sentences:
                yield f"data: {sentence}\n\n"
        except Exception as e:
            yield f"data: ⚠️ Error: {str(e)}\n\n"
        yield "event: close\ndata: \n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')
@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_query = request.json.get('query')  # Expects 'query' key
        if not user_query:
            return jsonify(error="Empty query"), 400
        return jsonify(
            stream_url=url_for('stream', q=user_query, _external=True)
        )
    except Exception as e:
        app.logger.error(f"Ask endpoint error: {str(e)}")
        return jsonify(error="Server error"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
