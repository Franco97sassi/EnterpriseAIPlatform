from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    user_query: str = Field(min_length=1)

    conversation_id: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    retrieved_context: list[dict[str, Any]] = Field(
        default_factory=list
    )


class AgentResponse(BaseModel):
    user_query: str

    selected_tool: str | None = None

    tool_result: Any = None

    requires_human_review: bool = False

    conversation_id: str | None = None