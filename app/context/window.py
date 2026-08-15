from app.context.compressor import ContextCompressor
from app.context.models import ContextItem


class ContextWindow:
    def __init__(
        self,
        max_characters: int,
        compressor: ContextCompressor | None = None,
    ):
        if max_characters <= 0:
            raise ValueError(
                "max_characters must be greater than zero."
            )

        self.max_characters = max_characters
        self.compressor = compressor

    def fit(
        self,
        items: list[ContextItem],
    ) -> list[ContextItem]:
        selected: list[ContextItem] = []
        used_characters = 0

        for item in items:
            remaining = self.max_characters - used_characters

            if remaining <= 0:
                break

            if len(item.content) <= remaining:
                selected.append(item)
                used_characters += len(item.content)
                continue

            if self.compressor is not None:
                compressed = self.compressor.compress(
                    item,
                    max_characters=remaining,
                )

                if compressed.content:
                    selected.append(compressed)
                    used_characters += len(compressed.content)

            break

        return selected