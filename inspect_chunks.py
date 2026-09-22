from modules.vector_store import VectorStore


vector_store = VectorStore()

results = vector_store.collection.get(
    include=["documents", "metadatas"]
)

documents = results["documents"]
metadatas = results["metadatas"]

print("\nTotal chunks:", len(documents))

for i in range(len(documents)):

    print("\n" + "=" * 70)

    print("Chunk:", i + 1)

    print("Document:", metadatas[i]["filename"])

    print("Page:", metadatas[i]["page_number"])

    print("\nText:")

    print(documents[i])