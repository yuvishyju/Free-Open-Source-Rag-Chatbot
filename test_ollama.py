from modules.ollama_client import OllamaClient


client = OllamaClient()

prompt = "What is machine learning? Explain in two sentences."

answer = client.generate(prompt)

print("\nOLLAMA ANSWER:")
print(answer)