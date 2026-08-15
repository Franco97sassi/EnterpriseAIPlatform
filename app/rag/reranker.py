from dataclasses import dataclass

from app.rag.hybrid_search import SearchResult


@dataclass(frozen=True)
class RerankedResult:
    result: SearchResult
    rerank_score: float


class Reranker:
    def rerank(
        self,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[RerankedResult]:
        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        reranked = [
            RerankedResult(
                result=result,
                rerank_score=result.hybrid_score,
            )
            for result in results
        ]

        reranked.sort(
            key=lambda item: item.rerank_score,
            reverse=True,
        )

        return reranked[:top_k]