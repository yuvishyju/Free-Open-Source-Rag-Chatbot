from modules.document_parser import extract_document
from modules.processing import process_document
from modules.embedding_service import EmbeddingService
from modules.vector_store import VectorStore


class DocumentIndexer:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def index_document(self, file_path, filename):

        print(f"Processing: {filename}")

        # Step 1: Extract text
        pages = extract_document(file_path)

        # Step 2: Clean and chunk
        chunks = process_document(
            pages,
            filename
        )

        if not chunks:
            return 0

        # Step 3: Generate embeddings
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_service.generate_embeddings(
            texts
        )

        # Step 4: Store in ChromaDB
        self.vector_store.add_chunks(
            chunks,
            embeddings
        )

        return len(chunks)