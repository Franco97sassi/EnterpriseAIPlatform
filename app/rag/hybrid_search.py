from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    document_id: str
    content: str
    semantic_score: float = 0.0
    lexical_score: float = 0.0

    @property
    def hybrid_score(self) -> float:
        return (
            self.semantic_score * 0.7
            + self.lexical_score * 0.3
        )


class HybridSearch:
    def rank(
        self,
        results: list[SearchResult],
    ) -> list[SearchResult]:
        return sorted(
            results,
            key=lambda result: result.hybrid_score,
            reverse=True,
        )