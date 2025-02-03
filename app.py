from flask import Flask, request, render_template, Response, stream_with_context, session, jsonify
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
    try:
        # Get current history or initialize
        chat_history = session.get('chat_history', [])
        
        # Store user query FIRST
        chat_history.append({
            'role': 'user',
            'parts': [user_query],
            'time': datetime.now().isoformat()
        })
        
        # Create context-aware prompt
        context_prompt = f"""
        Conversation History:
        {chat_history[-3:]}  # Keep last 3 exchanges
        
        New Query: {user_query[:500]}
        
        Respond to the current query while considering:
        1. Full conversation context
        2. Previous step numbers mentioned
        3. Any specific clarification requests
        """
        
        # Generate response with updated history
        chat = model.start_chat(history=chat_history)
        try:
            generation_config = {
                "temperature": 0.7,
            }
            response = chat.send_message(context_prompt, **generation_config)
            full_response = response.text
        except genai.APIError as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
        # Store AI response AFTER generation
        chat_history.append({
            'role': 'model',
            'parts': [full_response],
            'time': datetime.now().isoformat()
        })
        
        # Update session with new history
        session['chat_history'] = chat_history[-6:]  # Keep last 6 messages
        session.modified = True

        return full_response  # Return full response as a single string
        
    except Exception as e:
        return f"Error in generate_response: {str(e)}"  # Catch any errors in the function

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
