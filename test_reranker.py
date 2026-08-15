import pytest

from app.rag.hybrid_search import SearchResult
from app.rag.reranker import Reranker


def test_reranker_orders_results_by_score():
    reranker = Reranker()

    results = [
        SearchResult(
            document_id="doc-1",
            content="First",
            semantic_score=0.5,
            lexical_score=0.5,
        ),
        SearchResult(
            document_id="doc-2",
            content="Second",
            semantic_score=0.9,
            lexical_score=0.9,
        ),
    ]

    reranked = reranker.rerank(
        results,
        top_k=2,
    )

    assert reranked[0].result.document_id == "doc-2"
    assert reranked[1].result.document_id == "doc-1"


def test_reranker_respects_top_k():
    reranker = Reranker()

    results = [
        SearchResult(
            document_id=f"doc-{i}",
            content=f"Document {i}",
            semantic_score=0.9 - (i * 0.1),
            lexical_score=0.8,
        )
        for i in range(5)
    ]

    reranked = reranker.rerank(
        results,
        top_k=2,
    )

    assert len(reranked) == 2


def test_reranker_rejects_invalid_top_k():
    reranker = Reranker()

    with pytest.raises(
        ValueError,
        match="top_k must be greater than zero",
    ):
        reranker.rerank(
            [],
            top_k=0,
        )