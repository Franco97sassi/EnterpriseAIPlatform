from app.rag.hybrid_search import (
    HybridSearch,
    SearchResult,
)


def test_hybrid_score_combines_semantic_and_lexical_scores():
    result = SearchResult(
        document_id="doc-1",
        content="RAG combines retrieval and generation.",
        semantic_score=0.8,
        lexical_score=0.6,
    )

    assert result.hybrid_score == 0.74


def test_hybrid_search_ranks_results():
    search = HybridSearch()

    results = [
        SearchResult(
            document_id="doc-1",
            content="First",
            semantic_score=0.5,
            lexical_score=0.4,
        ),
        SearchResult(
            document_id="doc-2",
            content="Second",
            semantic_score=0.9,
            lexical_score=0.8,
        ),
    ]

    ranked = search.rank(results)

    assert ranked[0].document_id == "doc-2"
    assert ranked[1].document_id == "doc-1"


def test_hybrid_search_returns_empty_list():
    search = HybridSearch()

    ranked = search.rank([])

    assert ranked == []


def test_hybrid_search_can_promote_lexical_match():
    search = HybridSearch()

    results = [
        SearchResult(
            document_id="semantic",
            content="Semantic result",
            semantic_score=0.8,
            lexical_score=0.1,
        ),
        SearchResult(
            document_id="balanced",
            content="Balanced result",
            semantic_score=0.7,
            lexical_score=0.9,
        ),
    ]

    ranked = search.rank(results)

    assert ranked[0].document_id == "balanced"