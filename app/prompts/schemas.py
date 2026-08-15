from pydantic import BaseModel, Field


class AssistantResponse(BaseModel):
    answer: str = Field(min_length=1)
    grounded: bool
    confidence: float = Field(ge=0.0, le=1.0)