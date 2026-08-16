from app.agents.state import AgentState
from app.agents.tools import calculator_tool, semantic_search_tool


def agent_node(state: AgentState) -> AgentState:
    """
    Main agent decision node.

    For now routing is deterministic.
    Later we will replace/extend this with LLM tool calling.
    """
    query = state.get("user_query", "").strip()

    if not query:
        raise ValueError("user_query is required")

    query_lower = query.lower()

    calculator_keywords = (
        "calculate",
        "calculator",
        "sum",
        "add",
        "subtract",
        "multiply",
        "divide",
    )

    if any(keyword in query_lower for keyword in calculator_keywords):
        selected_tool = "calculator"
    else:
        selected_tool = "semantic_search"

    return {
        **state,
        "selected_tool": selected_tool,
    }


def tool_node(state: AgentState) -> AgentState:
    """
    Execute the tool selected by the agent node.
    """
    selected_tool = state.get("selected_tool")

    if not selected_tool:
        raise ValueError("selected_tool is required")

    query = state.get("user_query", "")

    if selected_tool == "semantic_search":
        result = semantic_search_tool(
            query=query,
            documents=state.get("retrieved_context", []),
        )

    elif selected_tool == "calculator":
        metadata = state.get("metadata", {})

        a = metadata.get("a")
        b = metadata.get("b")
        operation = metadata.get("operation")

        if a is None or b is None or operation is None:
            raise ValueError(
                "Calculator requires metadata fields: a, b and operation"
            )

        result = calculator_tool(
            a=a,
            b=b,
            operation=operation,
        )

    else:
        raise ValueError(f"Unknown tool: {selected_tool}")

    return {
        **state,
        "tool_result": result,
    }

def human_review_node(state: AgentState) -> AgentState:
    """
    Marks whether the current action requires human review.
    """
    selected_tool = state.get("selected_tool")

    requires_review = selected_tool == "calculator"

    return {
        **state,
        "requires_human_review": requires_review,
    }