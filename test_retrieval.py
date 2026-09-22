from modules.retriever import Retriever


retriever = Retriever()

question = "Who won the FIFA World Cup in 2022?"

results = retriever.search(
    question,
    top_k=4
)

if results is None:
    print("No relevant results found.")
    exit()

documents = results["documents"][0]
distances = results["distances"][0]
metadatas = results["metadatas"][0]

print("\nQUESTION:")
print(question)

print("\nRETRIEVED DOCUMENTS:")

for i in range(len(documents)):

    print("\n----------------------------")

    print("Result:", i + 1)
    print("Document:", metadatas[i]["filename"])
    print("Page:", metadatas[i]["page_number"])
    print("Distance:", distances[i])

    print("Text:")
    print(documents[i])