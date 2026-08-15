from app.context.manager import ContextManager
from app.context.memory import LongTermMemory, ShortTermMemory
from app.context.models import ContextItem


def test_context_manager_builds_combined_context():
    short_term = ShortTermMemory(max_items=3)
    long_term = LongTermMemory()

    short_term.add("User asked about RAG.")

    long_term.set(
        "preferred_style",
        "concise",
    )

    manager = ContextManager(
        short_term_memory=short_term,
        long_term_memory=long_term,
    )

    retrieved_items = [
        ContextItem(
            content="RAG combines retrieval and generation.",
            priority=10,
        )
    ]

    context = manager.build_context(
        retrieved_items=retrieved_items,
        max_characters=100,
    )

    assert "Short-term memory:" in context
    assert "User asked about RAG." in context

    assert "Long-term memory:" in context
    assert "preferred_style: concise" in context

    assert "Retrieved context:" in context
    assert "RAG combines retrieval and generation." in context


def test_context_manager_works_without_memory():
    manager = ContextManager(
        short_term_memory=ShortTermMemory(),
        long_term_memory=LongTermMemory(),
    )

    retrieved_items = [
        ContextItem(
            content="Enterprise AI context",
            priority=5,
        )
    ]

    context = manager.build_context(
        retrieved_items=retrieved_items,
        max_characters=100,
    )

    assert "Enterprise AI context" in context
    assert "Short-term memory:" not in context
    assert "Long-term memory:" not in context


def test_context_manager_respects_context_budget():
    manager = ContextManager(
        short_term_memory=ShortTermMemory(),
        long_term_memory=LongTermMemory(),
    )

    retrieved_items = [
        ContextItem(
            content="ABCDEFGHIJ",
            priority=10,
        )
    ]

    context = manager.build_context(
        retrieved_items=retrieved_items,
        max_characters=5,
        compress=True,
    )

    assert "AB..." in context
    assert "ABCDEFGHIJ" not in context