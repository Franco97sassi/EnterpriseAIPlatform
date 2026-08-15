from app.rag.hybrid_search import SearchResult
from app.rag.pipeline import AdvancedRAGPipeline


def test_advanced_rag_pipeline_prepares_queries():
    pipeline = AdvancedRAGPipeline()

    queries = pipeline.prepare_queries(
        "  What   is   RAG  ",
        count=3,
    )

    assert len(queries) == 3
    assert queries[0] == "What is RAG?"


def test_advanced_rag_pipeline_ranks_results():
    pipeline = AdvancedRAGPipeline()

    results = [
        SearchResult(
            document_id="doc-1",
            content="Low relevance",
            semantic_score=0.4,
            lexical_score=0.3,
        ),
        SearchResult(
            document_id="doc-2",
            content="High relevance",
            semantic_score=0.95,
            lexical_score=0.9,
        ),
    ]

    ranked = pipeline.rank_results(
        results,
        top_k=1,
    )

    assert len(ranked) == 1
    assert ranked[0].result.document_id == "doc-2"