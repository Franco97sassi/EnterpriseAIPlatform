from app.context.models import ContextItem


class MetadataFilter:
    def filter(
        self,
        items: list[ContextItem],
        filters: dict[str, str],
    ) -> list[ContextItem]:
        if not filters:
            return list(items)

        filtered_items: list[ContextItem] = []

        for item in items:
            matches = all(
                item.metadata.get(key) == value
                for key, value in filters.items()
            )

            if matches:
                filtered_items.append(item)

        return filtered_items