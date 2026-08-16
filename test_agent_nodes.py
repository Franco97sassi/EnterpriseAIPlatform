import pytest

from app.agents.nodes import agent_node


def test_agent_node_routes_to_calculator():
    state = {
        "messages": [],
        "user_query": "Calculate 10 plus 5",
        "metadata": {},
    }

    result = agent_node(state)

    assert result["selected_tool"] == "calculator"


def test_agent_node_routes_to_semantic_search():
    state = {
        "messages": [],
        "user_query": "What is retrieval augmented generation?",
        "metadata": {},
    }

    result = agent_node(state)

    assert result["selected_tool"] == "semantic_search"


def test_agent_node_preserves_state():
    state = {
        "messages": [],
        "user_query": "Explain LangGraph",
        "metadata": {"request_id": "123"},
    }

    result = agent_node(state)

    assert result["user_query"] == "Explain LangGraph"
    assert result["metadata"]["request_id"] == "123"


def test_agent_node_rejects_empty_query():
    state = {
        "messages": [],
        "user_query": "",
        "metadata": {},
    }

    with pytest.raises(ValueError):
        agent_node(state)