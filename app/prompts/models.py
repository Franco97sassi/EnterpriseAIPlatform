from dataclasses import dataclass, field
from typing import Type

from pydantic import BaseModel


@dataclass(frozen=True)
class PromptExample:
    input: str
    output: str


@dataclass(frozen=True)
class PromptDefinition:
    name: str
    version: str
    system_prompt: str
    user_template: str = ""
    examples: tuple[PromptExample, ...] = ()
    response_model: Type[BaseModel] | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def render_user_prompt(self, **kwargs: str) -> str:
        if not self.user_template:
            return ""

        try:
            return self.user_template.format(**kwargs)
        except KeyError as exc:
            missing_variable = exc.args[0]
            raise ValueError(
                f"Missing prompt variable: '{missing_variable}'"
            ) from exc

    def render_examples(self) -> str:
        if not self.examples:
            return ""

        sections = []

        for example in self.examples:
            sections.append(
                f"User:\n{example.input}\n\nAssistant:\n{example.output}"
            )

        return "\n\n---\n\n".join(sections)