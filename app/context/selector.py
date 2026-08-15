from app.context.compressor import ContextCompressor
from app.context.models import ContextItem
from app.context.window import ContextWindow


def select_context(
    items: list[ContextItem],
    limit: int,
) -> list[ContextItem]:
    if limit <= 0:
        return []

    sorted_items = sorted(
        items,
        key=lambda item: item.priority,
        reverse=True,
    )

    return sorted_items[:limit]


def select_context_with_budget(
    items: list[ContextItem],
    max_characters: int,
    compress: bool = False,
) -> list[ContextItem]:
    sorted_items = sorted(
        items,
        key=lambda item: item.priority,
        reverse=True,
    )

    compressor = ContextCompressor() if compress else None

    window = ContextWindow(
        max_characters=max_characters,
        compressor=compressor,
    )

    return window.fit(sorted_items)