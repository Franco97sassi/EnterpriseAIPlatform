from langgraph.graph import END, START, StateGraph

from app.agents.nodes import (
    agent_node,
    human_review_node,
    tool_node,
)
from app.agents.routing import route_after_review
from app.agents.state import AgentState


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("review_check", human_review_node)
    graph.add_node("tool", tool_node)

    graph.add_edge(START, "agent")
    graph.add_edge("agent", "review_check")

    graph.add_conditional_edges(
        "review_check",
        route_after_review,
        {
            "tool": "tool",
            "human_review": END,
        },
    )

    graph.add_edge("tool", END)

    return graph.compile()