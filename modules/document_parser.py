import pymupdf
from docx import Document


def extract_pdf(file_path):
    pages = []

    pdf = pymupdf.open(file_path)

    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text()

        pages.append({
            "text": text,
            "page_number": page_number
        })

    pdf.close()

    return pages


def extract_docx(file_path):
    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return [{
        "text": "\n".join(text),
        "page_number": None
    }]


def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [{
        "text": text,
        "page_number": None
    }]


def extract_document(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_docx(file_path)

    elif file_path.lower().endswith(".txt"):
        return extract_txt(file_path)

    else:
        raise ValueError("Unsupported file type")