from app.agents.graph import build_agent_graph
from app.agents.memory import AgentMemory
from app.agents.schemas import AgentRequest, AgentResponse


class AgentService:
    def __init__(self) -> None:
        self.graph = build_agent_graph()
        self.memory = AgentMemory()

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        conversation_id = request.conversation_id

        if conversation_id:
            self.memory.add_message(
                conversation_id=conversation_id,
                role="user",
                content=request.user_query,
            )

        initial_state = {
            "messages": [],
            "user_query": request.user_query,
            "metadata": request.metadata,
            "retrieved_context": request.retrieved_context,
        }

        result = self.graph.invoke(initial_state)

        return AgentResponse(
            user_query=result["user_query"],
            selected_tool=result.get("selected_tool"),
            tool_result=result.get("tool_result"),
            requires_human_review=result.get(
                "requires_human_review",
                False,
            ),
            conversation_id=conversation_id,
        )