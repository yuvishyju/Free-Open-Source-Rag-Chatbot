from modules.rag_engine import RAGEngine


def test_build_context_formatting():
    """Test that retrieved chunks are formatted with Document and Page citations."""
    rag = RAGEngine()

    mock_results = {
        "documents": [["The nominal voltage is 24 V DC."]],
        "metadatas": [[{
            "filename": "Servo_Manual.pdf",
            "page_number": 12,
            "document_id": "manual_1",
            "chunk_number": 1
        }]]
    }

    context = rag.build_context(mock_results)

    assert "Source: Servo_Manual.pdf, Page: 12" in context
    assert "The nominal voltage is 24 V DC." in context


def test_build_prompt_has_refusal_instruction():
    """Test that prompt contains the strict refusal rule to prevent hallucinations."""
    rag = RAGEngine()

    question = "What is the operating voltage?"
    context = "Source: Manual.pdf, Page: 1\nVoltage is 24V."

    prompt = rag.build_prompt(question, context)

    assert "I could not find this information in the uploaded documents." in prompt
    assert question in prompt
    assert context in prompt