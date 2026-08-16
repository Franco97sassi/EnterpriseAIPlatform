import pytest

from app.agents.tools import calculator_tool, semantic_search_tool


def test_semantic_search_tool():
    documents = [
        {"id": "1", "content": "RAG uses retrieval."},
        {"id": "2", "content": "Agents can use tools."},
    ]

    result = semantic_search_tool(
        query="What is RAG?",
        documents=documents,
    )

    assert result["tool"] == "semantic_search"
    assert result["query"] == "What is RAG?"
    assert result["count"] == 2
    assert len(result["documents"]) == 2


def test_semantic_search_tool_rejects_empty_query():
    with pytest.raises(ValueError):
        semantic_search_tool("")


def test_calculator_tool_add():
    result = calculator_tool(
        a=10,
        b=5,
        operation="add",
    )

    assert result["tool"] == "calculator"
    assert result["result"] == 15


def test_calculator_tool_divide():
    result = calculator_tool(
        a=10,
        b=2,
        operation="divide",
    )

    assert result["result"] == 5


def test_calculator_tool_rejects_division_by_zero():
    with pytest.raises(ValueError):
        calculator_tool(
            a=10,
            b=0,
            operation="divide",
        )


def test_calculator_tool_rejects_unknown_operation():
    with pytest.raises(ValueError):
        calculator_tool(
            a=10,
            b=2,
            operation="power",
        )