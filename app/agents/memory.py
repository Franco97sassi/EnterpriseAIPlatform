from copy import deepcopy
from typing import Any


class AgentMemory:
    """
    Simple in-memory conversation store.

    This will later be replaced or extended with persistent memory,
    Redis/PostgreSQL, or LangGraph checkpointing.
    """

    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:
        if not conversation_id.strip():
            raise ValueError("conversation_id cannot be empty")

        if role not in {"user", "assistant", "system", "tool"}:
            raise ValueError(f"Unsupported role: {role}")

        if not content.strip():
            raise ValueError("content cannot be empty")

        self._store.setdefault(conversation_id, [])

        self._store[conversation_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict[str, Any]]:
        return deepcopy(
            self._store.get(conversation_id, [])
        )

    def clear(
        self,
        conversation_id: str,
    ) -> None:
        self._store.pop(conversation_id, None)

    def exists(
        self,
        conversation_id: str,
    ) -> bool:
        return conversation_id in self._store