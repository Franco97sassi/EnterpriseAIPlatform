import pytest

from app.agents.nodes import tool_node


def test_tool_node_executes_semantic_search():
    state = {
        "messages": [],
        "user_query": "What is RAG?",
        "selected_tool": "semantic_search",
        "retrieved_context": [
            {"id": "1", "content": "RAG uses retrieval."}
        ],
        "metadata": {},
    }

    result = tool_node(state)

    assert result["tool_result"]["tool"] == "semantic_search"
    assert result["tool_result"]["count"] == 1


def test_tool_node_executes_calculator():
    state = {
        "messages": [],
        "user_query": "Calculate 10 plus 5",
        "selected_tool": "calculator",
        "metadata": {
            "a": 10,
            "b": 5,
            "operation": "add",
        },
    }

    result = tool_node(state)

    assert result["tool_result"]["tool"] == "calculator"
    assert result["tool_result"]["result"] == 15


def test_tool_node_rejects_missing_selected_tool():
    state = {
        "messages": [],
        "user_query": "Hello",
        "metadata": {},
    }

    with pytest.raises(ValueError):
        tool_node(state)


def test_tool_node_rejects_unknown_tool():
    state = {
        "messages": [],
        "user_query": "Hello",
        "selected_tool": "unknown_tool",
        "metadata": {},
    }

    with pytest.raises(ValueError):
        tool_node(state)


def test_tool_node_calculator_requires_metadata():
    state = {
        "messages": [],
        "user_query": "Calculate something",
        "selected_tool": "calculator",
        "metadata": {},
    }

    with pytest.raises(ValueError):
        tool_node(state)