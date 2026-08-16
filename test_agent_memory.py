import pytest

from app.agents.memory import AgentMemory


def test_memory_stores_messages():
    memory = AgentMemory()

    memory.add_message(
        conversation_id="conversation-1",
        role="user",
        content="What is RAG?",
    )

    messages = memory.get_messages("conversation-1")

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "What is RAG?"


def test_memory_preserves_conversation_history():
    memory = AgentMemory()

    memory.add_message(
        "conversation-1",
        "user",
        "What is RAG?",
    )

    memory.add_message(
        "conversation-1",
        "assistant",
        "RAG combines retrieval and generation.",
    )

    messages = memory.get_messages("conversation-1")

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_memory_separates_conversations():
    memory = AgentMemory()

    memory.add_message(
        "conversation-1",
        "user",
        "Hello",
    )

    memory.add_message(
        "conversation-2",
        "user",
        "Goodbye",
    )

    messages_1 = memory.get_messages("conversation-1")
    messages_2 = memory.get_messages("conversation-2")

    assert len(messages_1) == 1
    assert len(messages_2) == 1

    assert messages_1[0]["content"] == "Hello"
    assert messages_2[0]["content"] == "Goodbye"


def test_memory_can_be_cleared():
    memory = AgentMemory()

    memory.add_message(
        "conversation-1",
        "user",
        "Hello",
    )

    assert memory.exists("conversation-1") is True

    memory.clear("conversation-1")

    assert memory.exists("conversation-1") is False
    assert memory.get_messages("conversation-1") == []


def test_memory_rejects_invalid_role():
    memory = AgentMemory()

    with pytest.raises(ValueError):
        memory.add_message(
            "conversation-1",
            "invalid-role",
            "Hello",
        )


def test_memory_rejects_empty_content():
    memory = AgentMemory()

    with pytest.raises(ValueError):
        memory.add_message(
            "conversation-1",
            "user",
            "",
        )


def test_memory_rejects_empty_conversation_id():
    memory = AgentMemory()

    with pytest.raises(ValueError):
        memory.add_message(
            "",
            "user",
            "Hello",
        )