from dataclasses import dataclass

from app.context.memory import LongTermMemory, ShortTermMemory
from app.context.models import ContextItem
from app.context.selector import select_context_with_budget


@dataclass
class ContextManager:
    short_term_memory: ShortTermMemory
    long_term_memory: LongTermMemory

    def build_context(
        self,
        retrieved_items: list[ContextItem],
        max_characters: int,
        compress: bool = True,
    ) -> str:
        sections: list[str] = []

        short_term_items = self.short_term_memory.get_all()

        if short_term_items:
            sections.append(
                "Short-term memory:\n"
                + "\n".join(short_term_items)
            )

        long_term_items = self.long_term_memory.get_all()

        if long_term_items:
            formatted_memory = "\n".join(
                f"{key}: {value}"
                for key, value in long_term_items.items()
            )

            sections.append(
                "Long-term memory:\n"
                + formatted_memory
            )

        selected_context = select_context_with_budget(
            retrieved_items,
            max_characters=max_characters,
            compress=compress,
        )

        if selected_context:
            formatted_context = "\n".join(
                item.content
                for item in selected_context
            )

            sections.append(
                "Retrieved context:\n"
                + formatted_context
            )

        return "\n\n".join(sections)