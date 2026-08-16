from app.agents.state import AgentState


def test_agent_state_can_be_created():
    state: AgentState = {
        "messages": [],
        "user_query": "What is RAG?",
        "requires_human_review": False,
        "metadata": {},
    }

    assert state["user_query"] == "What is RAG?"
    assert state["messages"] == []
    assert state["requires_human_review"] is False


def test_agent_state_supports_tool_information():
    state: AgentState = {
        "messages": [],
        "selected_tool": "semantic_search",
        "tool_result": {"documents": ["doc1", "doc2"]},
    }

    assert state["selected_tool"] == "semantic_search"
    assert state["tool_result"]["documents"] == ["doc1", "doc2"]