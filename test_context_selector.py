import pytest

from app.context.models import ContextItem
from app.context.selector import (
    select_context,
    select_context_with_budget,
)
from app.context.window import ContextWindow


def test_select_context_by_priority():
    items = [
        ContextItem(
            content="Low priority",
            priority=1,
        ),
        ContextItem(
            content="High priority",
            priority=10,
        ),
        ContextItem(
            content="Medium priority",
            priority=5,
        ),
    ]

    selected = select_context(
        items,
        limit=2,
    )

    assert len(selected) == 2
    assert selected[0].content == "High priority"
    assert selected[1].content == "Medium priority"


def test_select_context_with_zero_limit():
    items = [
        ContextItem(
            content="Example",
            priority=1,
        )
    ]

    selected = select_context(
        items,
        limit=0,
    )

    assert selected == []


def test_context_window_respects_budget():
    items = [
        ContextItem(
            content="12345",
            priority=10,
        ),
        ContextItem(
            content="67890",
            priority=5,
        ),
        ContextItem(
            content="ABCDE",
            priority=1,
        ),
    ]

    selected = select_context_with_budget(
        items,
        max_characters=10,
    )

    assert len(selected) == 2
    assert selected[0].content == "12345"
    assert selected[1].content == "67890"


def test_context_window_prioritizes_important_content():
    items = [
        ContextItem(
            content="low",
            priority=1,
        ),
        ContextItem(
            content="important",
            priority=100,
        ),
    ]

    selected = select_context_with_budget(
        items,
        max_characters=9,
    )

    assert len(selected) == 1
    assert selected[0].content == "important"


def test_context_window_rejects_invalid_budget():
    with pytest.raises(
        ValueError,
        match="max_characters must be greater than zero",
    ):
        ContextWindow(max_characters=0)

from app.context.compressor import ContextCompressor


def test_context_compressor_shortens_content():
    compressor = ContextCompressor()

    item = ContextItem(
        content="This is a long piece of context.",
        priority=10,
        source="test",
    )

    compressed = compressor.compress(
        item,
        max_characters=10,
    )

    assert len(compressed.content) == 10
    assert compressed.content.endswith("...")
    assert compressed.priority == 10
    assert compressed.source == "test"


def test_context_compressor_keeps_short_content():
    compressor = ContextCompressor()

    item = ContextItem(
        content="Short",
        priority=5,
    )

    compressed = compressor.compress(
        item,
        max_characters=20,
    )

    assert compressed == item


def test_context_window_can_compress_remaining_content():
    items = [
        ContextItem(
            content="12345",
            priority=10,
        ),
        ContextItem(
            content="ABCDEFGHIJ",
            priority=5,
        ),
    ]

    selected = select_context_with_budget(
        items,
        max_characters=10,
        compress=True,
    )

    assert len(selected) == 2
    assert selected[0].content == "12345"
    assert len(selected[1].content) == 5