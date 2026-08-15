from app.rag.hybrid_search import HybridSearch, SearchResult
from app.rag.metadata_filter import MetadataFilter
from app.rag.multi_query import MultiQueryGenerator
from app.rag.query_rewriter import QueryRewriter
from app.rag.reranker import Reranker, RerankedResult


class AdvancedRAGPipeline:
    def __init__(self) -> None:
        self.query_rewriter = QueryRewriter()
        self.multi_query_generator = MultiQueryGenerator()
        self.metadata_filter = MetadataFilter()
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()

    def prepare_queries(
        self,
        query: str,
        count: int = 3,
    ) -> list[str]:
        rewritten = self.query_rewriter.rewrite(query)

        return self.multi_query_generator.generate(
            rewritten,
            count=count,
        )

    def rank_results(
        self,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[RerankedResult]:
        hybrid_ranked = self.hybrid_search.rank(results)

        return self.reranker.rerank(
            hybrid_ranked,
            top_k=top_k,
        )