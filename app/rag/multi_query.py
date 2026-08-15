from app.rag.query_rewriter import QueryRewriter


class MultiQueryGenerator:
    def __init__(self) -> None:
        self.rewriter = QueryRewriter()

    def generate(
        self,
        query: str,
        count: int = 3,
    ) -> list[str]:
        if count <= 0:
            raise ValueError(
                "count must be greater than zero."
            )

        base_query = self.rewriter.rewrite(query)

        queries = [base_query]

        if count >= 2:
            queries.append(
                f"Explain in detail: {base_query}"
            )

        if count >= 3:
            queries.append(
                f"Provide relevant information about: {base_query}"
            )

        return queries[:count]