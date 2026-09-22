import os
import pytest
from modules.document_parser import extract_document, extract_txt


def test_extract_txt_content(tmp_path):
    """Test that a TXT file is read correctly."""
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("This is a sample document for testing RAG.", encoding="utf-8")

    pages = extract_document(str(sample_file))

    assert len(pages) == 1
    assert "This is a sample document" in pages[0]["text"]
    assert pages[0]["page_number"] is None


def test_extract_txt_empty(tmp_path):
    """Test that an empty TXT file does not crash."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding="utf-8")

    pages = extract_document(str(empty_file))

    assert len(pages) == 1
    assert pages[0]["text"] == ""


def test_unsupported_file_extension():
    """Test that unsupported formats raise a ValueError."""
    with pytest.raises(ValueError) as exc_info:
        extract_document("document.unsupported_format")

    assert "Unsupported file type" in str(exc_info.value)