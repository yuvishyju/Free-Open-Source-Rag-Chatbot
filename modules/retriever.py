from modules.embedding_service import EmbeddingService
from modules.vector_store import VectorStore
from config import SIMILARITY_THRESHOLD, TOP_K


class Retriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def search(self, query, top_k=None, threshold=None):

        k = top_k if top_k is not None else TOP_K
        cutoff = threshold if threshold is not None else SIMILARITY_THRESHOLD

        # Convert the user's question into an embedding
        query_embedding = self.embedding_service.generate_query_embedding(query)

        # Search ChromaDB
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )

        # Check whether any results were returned
        if not results["distances"]:
            return None

        distances = results["distances"][0]

        if not distances:
            return None

        # Get the closest result
        best_distance = distances[0]

        # Reject the result if it is too dissimilar
        if best_distance > cutoff:
            return None

        return results