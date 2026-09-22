from modules.rag_engine import RAGEngine

rag = RAGEngine()

question = "What are tree terminologies?"

result = rag.ask(question)

print("\n==============================")
print("QUESTION")
print("==============================")
print(question)

print("\n==============================")
print("ANSWER")
print("==============================")
print(result["answer"])

print("\n==============================")
print("SOURCES")
print("==============================")

metadatas = result["results"]["metadatas"][0]
distances = result["results"]["distances"][0]

for i in range(len(metadatas)):

    metadata = metadatas[i]

    print(
        f"{i + 1}. "
        f"{metadata['filename']} "
        f"- Page {metadata['page_number']} "
        f"- Distance: {distances[i]:.4f}"
    )