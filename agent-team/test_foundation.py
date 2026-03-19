import os
from litellm import completion
from dotenv import load_dotenv
from typing import List, Dict

# Load API keys from .env
load_dotenv()

# Define model priorities by agent role
# Using direct providers (Gemini/Groq) to utilize your free-tier quotas
AGENT_MODEL_PRIORITIES = {
    "researcher": ["google_ai/gemini-1.5-flash", "groq/llama-3.1-8b-instant"],
    "coder": ["groq/llama-3.3-70b-versatile", "google_ai/gemini-1.5-flash"],
    "manager": ["google_ai/gemini-1.5-flash", "groq/llama-3.3-70b-versatile"]
}

def get_response(role: str, prompt: str):
    models = AGENT_MODEL_PRIORITIES.get(role, ["gemini/gemini-1.5-flash"])
    
    for model in models:
        try:
            print(f"Attempting {model} for {role}...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    
    return "All model attempts failed."

if __name__ == "__main__":
    print(get_response("researcher", "Hello, confirm you are working."))
