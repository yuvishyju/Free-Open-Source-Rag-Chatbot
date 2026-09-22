from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        print("Embedding model loaded.")

    def generate_embeddings(self, texts):
        """
        Convert a list of texts into numerical vectors.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings

    def generate_query_embedding(self, query):
        """
        Convert a single question into a numerical vector.
        """

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        return embedding[0]