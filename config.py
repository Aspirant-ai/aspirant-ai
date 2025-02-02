# config.py
import os
import google.generativeai as genai

def configure_ai():
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    return genai.GenerativeModel('gemini-pro')