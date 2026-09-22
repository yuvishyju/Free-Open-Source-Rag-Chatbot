import chromadb

from config import VECTOR_DB_PATH


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=VECTOR_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        print("ChromaDB initialized.")

    def add_chunks(self, chunks, embeddings):

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(chunk["chunk_id"])

            documents.append(chunk["text"])

            metadatas.append({
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "page_number": chunk["page_number"],
                "chunk_number": chunk["chunk_number"]
            })

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(
            f"Added {len(chunks)} chunks to ChromaDB."
        )

    def count(self):

        return self.collection.count()