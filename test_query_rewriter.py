import pytest

from app.rag.query_rewriter import QueryRewriter


def test_query_rewriter_cleans_whitespace():
    rewriter = QueryRewriter()

    rewritten = rewriter.rewrite(
        "  What   is   RAG  "
    )

    assert rewritten == "What is RAG?"


def test_query_rewriter_keeps_existing_question_mark():
    rewriter = QueryRewriter()

    rewritten = rewriter.rewrite(
        "What is RAG?"
    )

    assert rewritten == "What is RAG?"


def test_query_rewriter_rejects_empty_query():
    rewriter = QueryRewriter()

    with pytest.raises(
        ValueError,
        match="query must not be empty",
    ):
        rewriter.rewrite("   ")