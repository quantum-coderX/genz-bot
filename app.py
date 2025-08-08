from flask import Flask, request, jsonify
import random
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Giphy API key and URL
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
GIPHY_URL = "https://api.giphy.com/v1/gifs/search"

# Groq API key and endpoint
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Keywords for Giphy GIFs
gif_keywords = ["vibes", "slay", "yolo", "lit", "mood"]

def get_random_gif():
    try:
        keyword = random.choice(gif_keywords)
        params = {"api_key": GIPHY_API_KEY, "q": keyword, "limit": 1, "rating": "pg"}
        response = requests.get(GIPHY_URL, params=params)
        data = response.json()
        if data["data"]:
            return data["data"][0]["images"]["fixed_height"]["url"]
        return None
    except:
        return None

def get_groq_response(user_message):
    try:
        # Prompt for Gen Z-style response
        prompt = (
            f"You are a Gen Z texter bot. Respond to '{user_message}' "
            "in 10 words or less, using Gen Z slang and emojis. "
            "Be casual, fun, and trendy."
        )
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",  # Confirmed working model
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 20,  # Keep it short
            "temperature": 0.8  # Add creativity
        }
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error with Groq API: {e}")
        print(f"Response status: {getattr(response, 'status_code', 'N/A')}")
        print(f"Response text: {getattr(response, 'text', 'N/A')}")
        return "Lowkey broke, try again? 🤔"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    bot_response = get_groq_response(user_message)
    
    # 30% chance to include a GIF
    if random.random() < 0.3:
        gif_url = get_random_gif()
        if gif_url:
            bot_response += f" <img src='{gif_url}' alt='GIF' style='max-width: 200px; border-radius: 10px;'>"
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)