from modules.embedding_service import EmbeddingService


embedding_service = EmbeddingService()


texts = [
    "The recommended operating voltage is 24 volts DC.",
    "The system requires a power supply of 24 volts."
]


embeddings = embedding_service.generate_embeddings(texts)


print("Number of texts:", len(texts))

print("Embedding shape:", embeddings.shape)

print("First embedding:")
print(embeddings[0])