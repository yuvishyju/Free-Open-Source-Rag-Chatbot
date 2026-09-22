import os

from modules.text_cleaner import clean_text
from modules.chunker import create_chunks


def process_document(pages, filename):
    """
    Clean extracted pages and convert them into chunks.
    """

    document_id = os.path.splitext(filename)[0]

    all_chunks = []

    for page in pages:

        raw_text = page["text"]

        page_number = page["page_number"]

        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            continue

        chunks = create_chunks(
            text=cleaned_text,
            filename=filename,
            document_id=document_id,
            page_number=page_number
        )

        all_chunks.extend(chunks)

    return all_chunks