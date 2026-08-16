from app.agents.graph import build_agent_graph


def test_graph_executes_semantic_search_flow():
    graph = build_agent_graph()

    initial_state = {
        "messages": [],
        "user_query": "What is RAG?",
        "retrieved_context": [
            {
                "id": "1",
                "content": "RAG combines retrieval and generation.",
            }
        ],
        "metadata": {},
    }

    result = graph.invoke(initial_state)

    assert result["selected_tool"] == "semantic_search"
    assert result["tool_result"]["tool"] == "semantic_search"
    assert result["tool_result"]["count"] == 1


def test_graph_routes_calculator_to_human_review():
    graph = build_agent_graph()

    initial_state = {
        "messages": [],
        "user_query": "Calculate 10 plus 5",
        "metadata": {
            "a": 10,
            "b": 5,
            "operation": "add",
        },
    }

    result = graph.invoke(initial_state)

    assert result["selected_tool"] == "calculator"
    assert result["requires_human_review"] is True
    assert "tool_result" not in result


def test_graph_preserves_original_query():
    graph = build_agent_graph()

    initial_state = {
        "messages": [],
        "user_query": "Explain LangGraph",
        "metadata": {},
    }

    result = graph.invoke(initial_state)

    assert result["user_query"] == "Explain LangGraph"