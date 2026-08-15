from fastapi.testclient import TestClient

from app.api import chat
from app.main import app
from app.models.analysis import TextAnalysis


client = TestClient(app)


async def mock_generate(prompt: str) -> str:
    return "mocked response"


async def mock_analyze_text(text: str) -> TextAnalysis:
    return TextAnalysis(
        summary="Mock summary",
        sentiment="positive",
        main_topic="FastAPI",
    )


def test_chat(monkeypatch):
    monkeypatch.setattr(
        chat.provider,
        "generate",
        mock_generate,
    )

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "response": "mocked response",
        "provider": "gemini",
    }


def test_chat_validation():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_analyze_text(monkeypatch):
    monkeypatch.setattr(
        chat.provider,
        "analyze_text",
        mock_analyze_text,
    )

    response = client.post(
        "/api/v1/chat/analyze",
        json={
            "message": "FastAPI is great.",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Mock summary",
        "sentiment": "positive",
        "main_topic": "FastAPI",
    }