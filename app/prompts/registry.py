from app.prompts.models import PromptDefinition
from app.prompts.versions.assistant_v1 import ASSISTANT_V1
from app.prompts.versions.assistant_v2 import ASSISTANT_V2


PROMPT_REGISTRY: dict[str, PromptDefinition] = {
    "assistant:v1": ASSISTANT_V1,
    "assistant:v2": ASSISTANT_V2,
}


def get_prompt(name: str, version: str) -> PromptDefinition:
    key = f"{name}:{version}"

    try:
        return PROMPT_REGISTRY[key]
    except KeyError as exc:
        raise ValueError(
            f"Prompt '{name}' version '{version}' does not exist."
        ) from exc