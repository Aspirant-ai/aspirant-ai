# Aspirant AI - AI-Powered Learning Assistant

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An intelligent learning platform leveraging Google's Gemini AI to generate practice questions and explain complex concepts in simple terms.

## Features 
- Dynamic question generation for competitive exams
- Concept explanation with real-life examples
- Adaptive difficulty levels
- Web-based interface

## Installation 
```bash
git clone https://github.com/Aspirant-ai/aspirant-ai.git
cd aspirant-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration 
1. Create `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
```
2. Get Gemini API key: [Google AI Studio](https://aistudio.google.com/)

## Deployment 
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Required Render settings:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `pip install gunicorn && gunicorn gunicorn_server:app`

## Usage 
```python
# Sample API Request
import requests

# Generate questions
response = requests.post('https://aspirant-ai.onrender.com/generate_questions', 
    json={'topic': 'Quantum Mechanics'})

# Ask doubt
response = requests.post('https://aspirant-ai.onrender.com/ask_doubt',
    json={'question': 'Explain Schrödinger equation'})
```

## Project Structure 
```
aspirant-ai/
├── app.py               # Main Flask application
├── templates/           # HTML templates
│   └── index.html
├── static/              # CSS/JS assets
│   ├── style.css
│   └── script.js
├── requirements.txt     # Dependencies
└── gunicorn_server.py   # Production server config
```

## Tech Stack 
- **Backend:** Flask + Gemini AI
- **Frontend:** HTML5/CSS3 + Vanilla JS
- **Hosting:** Render
- **WSGI Server:** Gunicorn

## Contributing 
Pull requests welcome! Please follow PEP8 guidelines.

## License 
MIT License - See [LICENSE](LICENSE)

## Contact 📬

**Support Channels:**
- 📧 Email: [support](#)
- 🐛 GitHub Issues: [Report Bugs/Requests](https://github.com/Aspirant-ai/aspirant-ai/issues)
- 💬 Community Discord: [Join Discussion](#)


