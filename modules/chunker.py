from config import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(
    text,
    filename,
    document_id,
    page_number=None,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
):
    """
    Split text into overlapping chunks
    and attach metadata.
    """

    words = text.split()

    chunks = []

    start = 0
    chunk_number = 1

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        if chunk_text.strip():

            chunk_id = (
                f"{document_id}_"
                f"page_{page_number}_"
                f"chunk_{chunk_number}"
            )

            chunks.append({
                "chunk_id": chunk_id,
                "document_id": document_id,
                "filename": filename,
                "page_number": page_number,
                "chunk_number": chunk_number,
                "text": chunk_text
            })

            chunk_number += 1

        start = end - overlap

    return chunks