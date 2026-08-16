from app.agents.state import AgentState


def route_after_review(state: AgentState) -> str:
    """
    Decide whether execution can continue automatically
    or should stop for human review.
    """
    if state.get("requires_human_review", False):
        return "human_review"

    return "tool"