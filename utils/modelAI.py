# utils/gemini_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def gemini_model():
    AI_KEY = os.getenv("AI_API_KEY")
    genai.configure(api_key=AI_KEY)
    return genai.GenerativeModel("gemini-2.0-flash")
