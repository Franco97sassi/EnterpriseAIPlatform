from app.context.models import ContextItem


class ContextCompressor:
    def compress(
        self,
        item: ContextItem,
        max_characters: int,
    ) -> ContextItem:
        if max_characters <= 0:
            raise ValueError(
                "max_characters must be greater than zero."
            )

        if len(item.content) <= max_characters:
            return item

        if max_characters <= 3:
            compressed_content = item.content[:max_characters]
        else:
            compressed_content = (
                item.content[: max_characters - 3] + "..."
            )

        return ContextItem(
            content=compressed_content,
            priority=item.priority,
            source=item.source,
        )