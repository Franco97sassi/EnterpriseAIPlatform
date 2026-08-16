from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]

    user_query: str

    rewritten_query: str

    retrieved_context: list[dict[str, Any]]

    selected_tool: str | None

    tool_result: Any

    final_answer: str | None

    requires_human_review: bool

    metadata: dict[str, Any]