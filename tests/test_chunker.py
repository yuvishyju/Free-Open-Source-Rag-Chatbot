from modules.chunker import create_chunks


def test_create_chunks_basic():
    """Test that text is split into chunks with correct metadata."""
    sample_text = "word " * 100  # 100 words

    chunks = create_chunks(
        text=sample_text,
        filename="test_manual.pdf",
        document_id="manual_001",
        page_number=1,
        chunk_size=50,
        overlap=10
    )

    # 100 words with chunk_size 50 and overlap 10 should produce multiple chunks
    assert len(chunks) >= 2

    first_chunk = chunks[0]
    assert first_chunk["filename"] == "test_manual.pdf"
    assert first_chunk["document_id"] == "manual_001"
    assert first_chunk["page_number"] == 1
    assert first_chunk["chunk_number"] == 1
    assert "chunk_id" in first_chunk


def test_chunk_overlap_preservation():
    """Test that the end of chunk 1 appears at the start of chunk 2."""
    words = [f"word{i}" for i in range(1, 31)]  # 30 words
    sample_text = " ".join(words)

    chunks = create_chunks(
        text=sample_text,
        filename="test.txt",
        document_id="doc_1",
        chunk_size=15,
        overlap=5
    )

    # Words 11-15 should appear in both chunk 1 and chunk 2 because overlap is 5
    chunk1_text = chunks[0]["text"]
    chunk2_text = chunks[1]["text"]

    assert "word11" in chunk1_text
    assert "word11" in chunk2_text


def test_empty_text_chunks():
    """Test that empty text yields 0 chunks."""
    chunks = create_chunks(
        text="   ",
        filename="empty.txt",
        document_id="empty_doc"
    )
    assert len(chunks) == 0