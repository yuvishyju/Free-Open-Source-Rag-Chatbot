import requests
from config import OLLAMA_URL, OLLAMA_MODEL


class OllamaClient:

    def __init__(self, model=None):
        self.url = OLLAMA_URL
        self.model = model or OLLAMA_MODEL

    def generate(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]