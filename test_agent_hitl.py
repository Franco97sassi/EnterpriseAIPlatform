from app.agents.graph import build_agent_graph
from app.agents.nodes import human_review_node
from app.agents.routing import route_after_review


def test_human_review_node_requires_review_for_calculator():
    state = {
        "messages": [],
        "user_query": "Calculate 10 plus 5",
        "selected_tool": "calculator",
        "metadata": {},
    }

    result = human_review_node(state)

    assert result["requires_human_review"] is True


def test_human_review_node_allows_semantic_search():
    state = {
        "messages": [],
        "user_query": "What is RAG?",
        "selected_tool": "semantic_search",
        "metadata": {},
    }

    result = human_review_node(state)

    assert result["requires_human_review"] is False


def test_route_after_review_returns_human_review():
    state = {
        "requires_human_review": True,
    }

    assert route_after_review(state) == "human_review"


def test_route_after_review_returns_tool():
    state = {
        "requires_human_review": False,
    }

    assert route_after_review(state) == "tool"


def test_graph_stops_before_calculator_tool():
    graph = build_agent_graph()

    state = {
        "messages": [],
        "user_query": "Calculate 10 plus 5",
        "metadata": {
            "a": 10,
            "b": 5,
            "operation": "add",
        },
    }

    result = graph.invoke(state)

    assert result["selected_tool"] == "calculator"
    assert result["requires_human_review"] is True
    assert "tool_result" not in result


def test_graph_executes_semantic_search_without_review():
    graph = build_agent_graph()

    state = {
        "messages": [],
        "user_query": "Explain RAG",
        "retrieved_context": [
            {
                "id": "1",
                "content": "RAG combines retrieval and generation.",
            }
        ],
        "metadata": {},
    }

    result = graph.invoke(state)

    assert result["selected_tool"] == "semantic_search"
    assert result["requires_human_review"] is False
    assert result["tool_result"]["tool"] == "semantic_search"