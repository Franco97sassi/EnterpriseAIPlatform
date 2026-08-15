import re


class QueryRewriter:
    def rewrite(self, query: str) -> str:
        cleaned = query.strip()

        if not cleaned:
            raise ValueError("query must not be empty.")

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        )

        if cleaned[-1] not in ".?!":
            cleaned += "?"

        return cleaned