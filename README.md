# ✨ Aspirant AI - AI-Powered Learning Assistant 🚀

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license)
![Platform](https://img.shields.io/badge/platform-Web%20%7C%20Telegram-blueviolet)

[![ASPIRANT AI profile views](https://u8views.com/api/v1/github/profiles/155420983/views/day-week-month-total-count.svg)](https://u8views.com/github/Aspirant-ai)

> **Empowering learners with AI-driven education!** 📚✨

Aspirant AI is an intelligent learning platform leveraging Google's **Gemini AI** to generate practice questions, explain complex concepts, and now available both **as a website and Telegram bot**! 🎉

---

## 🌟 Features 
✅ Dynamic question generation for competitive exams  
✅ Concept explanations with real-life examples  
✅ Adaptive difficulty levels for personalized learning  
✅ **Web-based Interface & Fully Functional Telegram Bot** 🤖  
✅ Sleek, modern UI for seamless interaction  
✅ Supports multiple subjects and topics  

---

## 🔥 Installation & Setup

```bash
git clone https://github.com/Aspirant-ai/aspirant-ai.git
cd aspirant-ai
python -m venv venv
venv\Scripts\activate  # For Windows
source venv/bin/activate  # For macOS/Linux
pip install -r requirements.txt
```

---

## ⚙️ Configuration 
1. Create a `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```
2. Get your **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).  
3. Obtain your **Telegram Bot Token** from [BotFather](https://t.me/BotFather).  

---

## 🚀 Deployment & Hosting

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Render Configuration:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `pip install gunicorn && gunicorn gunicorn_server:app`

---

## 🎯 How to Use

### 🌍 Web Interface
Simply visit: **[Aspirant AI Web](https://aspirant-ai.onrender.com/)** and start learning! 🖥️

### 🤖 Telegram Bot Commands
- `/start` - Start the bot
- `/generate <topic>` - Generate AI-powered questions on any topic
- `/ask <question>` - Get AI-powered explanations
- `/help` - Get assistance on how to use the bot

---

## 📁 Project Structure 
```
aspirant-ai/
├── app.py               # Main Flask application
├── telegram_bot.py      # Telegram Bot Integration
├── templates/           # HTML templates
│   └── index.html
├── static/              # CSS/JS assets
│   ├── style.css
│   └── script.js
├── requirements.txt     # Dependencies
└── gunicorn_server.py   # Production server config
```

---

## 🛠 Tech Stack 
🔹 **Backend:** Flask + Gemini AI  
🔹 **Frontend:** HTML5/CSS3 + JavaScript  
🔹 **Bot:** Telegram API Integration  
🔹 **Hosting:** Render (Auto-deploy)  
🔹 **WSGI Server:** Gunicorn  

---

## 🏆 Contributing 
We welcome contributions! 🚀 If you'd like to contribute:
1. Fork the repo
2. Create a feature branch
3. Commit and push your changes
4. Open a PR!

**Please follow PEP8 coding guidelines.**

---

## 📬 Contact & Support
📧 Email: [support](#)  
🐛 GitHub Issues: [Report Bugs/Requests](https://github.com/Aspirant-ai/aspirant-ai/issues)  
💬 Community Discord: [Join Discussion](#)  

---

🌟 **Join us on this AI-powered learning journey and supercharge your education!** 🚀📚
