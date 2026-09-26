from modules.retriever import Retriever
from modules.ollama_client import OllamaClient
from config import TOP_K


class RAGEngine:

    def __init__(self):
        self.retriever = Retriever()
        self.ollama = OllamaClient()

    def build_context(self, results):

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context_parts = []

        for i in range(len(documents)):

            document = documents[i]
            metadata = metadatas[i]

            filename = metadata.get("filename", "Unknown document")
            page_number = metadata.get("page_number", None)

            source = f"Source: {filename}"

            if page_number is not None:
                source += f", Page: {page_number}"

            context_parts.append(
                f"{source}\n{document}"
            )

        context = "\n\n".join(context_parts)

        return context

    def build_prompt(self, question, context):

        prompt = f"""
You are a document question-answering assistant.

Answer the question ONLY using the information provided in the context.

Do not use outside knowledge.
Do not invent or assume information.

If the answer cannot be found in the context, say:

"I could not find this information in the uploaded documents."

Mention the source document and page number when available.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        return prompt

    def ask(self, question):

        results = self.retriever.search(
            question,
            top_k=TOP_K
        )

        if results is None:
            return {
                "answer": "I could not find this information in the uploaded documents.",
                "results": None,
                "context": ""
            }

        context = self.build_context(results)

        prompt = self.build_prompt(
            question,
            context
        )

        answer = self.ollama.generate(prompt)

        return {
            "answer": answer,
            "results": results,
            "context": context
        }