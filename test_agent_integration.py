from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_agent_semantic_search_endpoint():
    response = client.post(
        "/api/v1/agents/run",
        json={
            "user_query": "What is RAG?",
            "retrieved_context": [
                {
                    "id": "1",
                    "content": "RAG combines retrieval and generation.",
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["selected_tool"] == "semantic_search"
    assert data["requires_human_review"] is False
    assert data["tool_result"]["tool"] == "semantic_search"
    assert data["tool_result"]["count"] == 1


def test_agent_hitl_endpoint():
    response = client.post(
        "/api/v1/agents/run",
        json={
            "user_query": "Calculate 10 plus 5",
            "metadata": {
                "a": 10,
                "b": 5,
                "operation": "add",
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["selected_tool"] == "calculator"
    assert data["requires_human_review"] is True
    assert data["tool_result"] is None


def test_agent_conversation_id():
    response = client.post(
        "/api/v1/agents/run",
        json={
            "user_query": "Explain LangGraph",
            "conversation_id": "integration-test-123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] == "integration-test-123"


def test_agent_rejects_empty_query():
    response = client.post(
        "/api/v1/agents/run",
        json={
            "user_query": "",
        },
    )

    assert response.status_code == 422