from flask import Flask, request, render_template, Response, stream_with_context, session
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
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 2048
        }

        # Safe prompt construction
        safe_prompt = f"""
        **User Query:** {user_query[:500]}  # Limit input length
        
        Provide a helpful response with:
        - Clear organization
        - Practical examples
        - Actionable steps
        - Markdown formatting"""

        chat = model.start_chat(history=session.get('chat_history', []))
        response = chat.send_message(
            safe_prompt,
            stream=True,
            generation_config=generation_config,
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
            }
        )
        
        full_response = []
        for chunk in response:
            if chunk.text:
                text = chunk.text.replace('\n\n', '\n')
                full_response.append(text)
                yield text
                
        session.setdefault('chat_history', []).append({
            'role': 'model',
            'parts': ['\n'.join(full_response)],
            'time': datetime.now().isoformat()
        })
        session.modified = True

    except Exception as e:
        app.logger.error(f"Generation Error: {str(e)}")
        yield f"⚠️ Error: {str(e)}" if app.debug else "⚠️ Service unavailable"

@app.before_request
def init_session():
    session.setdefault('chat_history', [])

# Rest of the routes remain same as in your code...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        try:
            user_query = request.args.get('q')
            for chunk in generate_response(user_query):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: ⚠️ Error: {str(e)}\n\n"
        finally:
            yield "event: close\ndata: \n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return Response("Empty message", status=400)
            
        def generate():
            try:
                for chunk in generate_response(user_message):
                    yield f"data: {chunk}\n\n"
            except Exception as e:
                yield f"data: ⚠️ Error: {str(e)}\n\n"
            finally:
                yield "event: close\ndata: \n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
        
    except Exception as e:
        app.logger.error(f"Ask endpoint error: {str(e)}")
        return Response("Server error", status=500)

@app.before_request
def check_session():
    if 'chat_history' not in session:
        session['chat_history'] = []

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)