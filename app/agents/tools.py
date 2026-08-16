from typing import Any


def semantic_search_tool(
    query: str,
    documents: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Temporary semantic search tool.

    Later this tool will be connected to the existing
    semantic search / RAG pipeline.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")

    documents = documents or []

    return {
        "tool": "semantic_search",
        "query": query,
        "documents": documents,
        "count": len(documents),
    }


def calculator_tool(a: float, b: float, operation: str) -> dict[str, Any]:
    """
    Simple deterministic calculator tool.
    """
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else None,
    }

    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")

    if operation == "divide" and b == 0:
        raise ValueError("Cannot divide by zero")

    return {
        "tool": "calculator",
        "operation": operation,
        "result": operations[operation],
    }