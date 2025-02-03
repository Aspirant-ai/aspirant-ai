from flask import Flask, request, render_template, Response, stream_with_context, session
import time
import os
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__, static_folder="static")

# Configure Generative AI
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def generate_response(user_query):
    """Generates actual AI responses using Gemini Pro"""
    try:
        # Start chat session
        chat = model.start_chat(history=[])
        
        # Stream responses from AI
        response = chat.send_message(user_query, stream=True)
        
        # Yield actual response chunks
        for chunk in response:
            yield chunk.text
    
    except Exception as e:
        app.logger.error(f"AI Error: {str(e)}")
        yield "⚠️ Could not generate response. Please try again."

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
    data = request.get_json()
    user_message = data.get('message', '')
    
    def generate():
        try:
            for chunk in generate_response(user_message):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: ⚠️ Error: {str(e)}\n\n"
        finally:
            yield "event: close\ndata: \n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)