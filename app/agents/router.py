from fastapi import APIRouter

from app.agents.schemas import AgentRequest, AgentResponse
from app.agents.service import AgentService


router = APIRouter(
    prefix="/api/v1/agents",
    tags=["agents"],
)

agent_service = AgentService()


@router.post(
    "/run",
    response_model=AgentResponse,
)
def run_agent(
    request: AgentRequest,
) -> AgentResponse:
    return agent_service.run(request)