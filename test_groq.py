import os
import requests
from dotenv import load_dotenv
import sys

# Load environment variables
print(f"Current working directory: {os.getcwd()}")
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found in environment variables.")
    print("Checking .env file directly...")
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            print(f"Env file content: {env_content}")
    except Exception as e:
        print(f"Error reading .env file: {e}")
    sys.exit(1)

print(f"Using API key: {GROQ_API_KEY[:5]}...{GROQ_API_KEY[-5:]}")

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Prepare headers and payload
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Try different model names
models_to_try = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

# Test simple prompt with each model
for model in models_to_try:
    print(f"\nTesting model: {model}")
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say hello in a short, fun way"}],
        "max_tokens": 20,
        "temperature": 0.7
    }
    
    try:
        # Make the request
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        print(f"Status code: {response.status_code}")
        
        # Check if successful
        if response.status_code == 200:
            data = response.json()
            message = data["choices"][0]["message"]["content"].strip()
            print(f"Response: {message}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
