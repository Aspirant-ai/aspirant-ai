from flask import Flask, request, render_template, Response, stream_with_context
import time
import os
from markupsafe import Markup
import markdown2

app = Flask(__name__)

# Configure logging
app.logger.setLevel('INFO')

def generate_response(user_query):
    """Generates streaming response with progress indicators"""
    try:
        # Example response sequence - replace with actual AI integration
        responses = [
            f"🔍 Analyzing your query: '{user_query}'...\n",
            "📚 Accessing knowledge base...\n",
            "🧠 Processing with AI models...\n",
            "✨ Crafting detailed explanation...\n",
            "✅ Finalizing response...\n"
        ]
        
        for part in responses:
            yield part
            time.sleep(0.8)  # Simulate processing time
            
    except Exception as e:
        app.logger.error(f"Response generation error: {str(e)}")
        yield "⚠️ Error generating response. Please try again."

@app.route('/')
def index():
    """Main chat interface endpoint"""
    return render_template('index.html')

@app.route('/stream')
def stream():
    """SSE endpoint for streaming responses"""
    def generate():
        try:
            user_query = request.args.get('q')
            for chunk in generate_response(user_query):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            app.logger.error(f"Stream error: {str(e)}")
            yield f"data: ⚠️ Error: {str(e)}\n\n"
        finally:
            yield "event: close\ndata: \n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/ask', methods=['POST'])
def ask():
    """Chat message processing endpoint"""
    try:
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
    
    except Exception as e:
        app.logger.error(f"Ask endpoint error: {str(e)}")
        return Response("Server error", status=500)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)