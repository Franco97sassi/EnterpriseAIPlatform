from app.context.memory import (
    LongTermMemory,
    ShortTermMemory,
)


def test_short_term_memory_stores_messages():
    memory = ShortTermMemory(max_items=3)

    memory.add("Hello")
    memory.add("How are you?")

    assert memory.get_all() == [
        "Hello",
        "How are you?",
    ]


def test_short_term_memory_respects_max_items():
    memory = ShortTermMemory(max_items=2)

    memory.add("Message 1")
    memory.add("Message 2")
    memory.add("Message 3")

    assert memory.get_all() == [
        "Message 2",
        "Message 3",
    ]


def test_long_term_memory_stores_values():
    memory = LongTermMemory()

    memory.set(
        "preferred_language",
        "English",
    )

    assert memory.get("preferred_language") == "English"


def test_long_term_memory_returns_none_for_unknown_key():
    memory = LongTermMemory()

    assert memory.get("unknown") is None


def test_long_term_memory_overwrites_existing_value():
    memory = LongTermMemory()

    memory.set("project", "AI Platform")
    memory.set("project", "Enterprise AI Platform")

    assert memory.get("project") == "Enterprise AI Platform"