from dataclasses import dataclass, field


@dataclass(frozen=True)
class MemoryItem:
    key: str
    value: str


@dataclass
class ShortTermMemory:
    max_items: int = 10
    items: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.items.append(message)

        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]

    def get_all(self) -> list[str]:
        return list(self.items)


@dataclass
class LongTermMemory:
    items: dict[str, str] = field(default_factory=dict)

    def set(self, key: str, value: str) -> None:
        self.items[key] = value

    def get(self, key: str) -> str | None:
        return self.items.get(key)

    def get_all(self) -> dict[str, str]:
        return dict(self.items)