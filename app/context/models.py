from dataclasses import dataclass, field


@dataclass(frozen=True)
class ContextItem:
    content: str
    priority: int = 0
    source: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)