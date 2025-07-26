# ollama_client.py
import requests

def ask_ollama(prompt, model="tinyllama"):
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return res.json().get("response", "No response")
    except Exception as e:
        return f"Error: {str(e)}"
