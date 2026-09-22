import re


def clean_text(text):
    """
    Clean extracted document text.
    """

    # Replace multiple spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple newlines with one newline
    text = re.sub(r"\n+", "\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text