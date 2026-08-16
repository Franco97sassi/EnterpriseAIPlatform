from app.agents.schemas import AgentRequest
from app.agents.service import AgentService


def test_agent_service_executes_semantic_search():
    service = AgentService()

    request = AgentRequest(
        user_query="What is RAG?",
        retrieved_context=[
            {
                "id": "1",
                "content": "RAG combines retrieval and generation.",
            }
        ],
    )

    response = service.run(request)

    assert response.user_query == "What is RAG?"
    assert response.selected_tool == "semantic_search"
    assert response.requires_human_review is False
    assert response.tool_result["tool"] == "semantic_search"


def test_agent_service_detects_human_review():
    service = AgentService()

    request = AgentRequest(
        user_query="Calculate 10 plus 5",
        metadata={
            "a": 10,
            "b": 5,
            "operation": "add",
        },
    )

    response = service.run(request)

    assert response.selected_tool == "calculator"
    assert response.requires_human_review is True
    assert response.tool_result is None


def test_agent_service_stores_user_message():
    service = AgentService()

    request = AgentRequest(
        user_query="Explain LangGraph",
        conversation_id="conversation-123",
    )

    service.run(request)

    messages = service.memory.get_messages(
        "conversation-123"
    )

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Explain LangGraph"