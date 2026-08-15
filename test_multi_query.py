import pytest

from app.rag.multi_query import MultiQueryGenerator


def test_multi_query_generates_requested_queries():
    generator = MultiQueryGenerator()

    queries = generator.generate(
        "What is RAG",
        count=3,
    )

    assert len(queries) == 3

    assert queries[0] == "What is RAG?"
    assert "Explain in detail" in queries[1]
    assert "Provide relevant information" in queries[2]


def test_multi_query_uses_rewritten_query():
    generator = MultiQueryGenerator()

    queries = generator.generate(
        "  What   is   RAG  ",
        count=2,
    )

    assert queries[0] == "What is RAG?"
    assert "What is RAG?" in queries[1]


def test_multi_query_supports_single_query():
    generator = MultiQueryGenerator()

    queries = generator.generate(
        "What is RAG?",
        count=1,
    )

    assert queries == [
        "What is RAG?"
    ]


def test_multi_query_rejects_invalid_count():
    generator = MultiQueryGenerator()

    with pytest.raises(
        ValueError,
        match="count must be greater than zero",
    ):
        generator.generate(
            "What is RAG?",
            count=0,
        )