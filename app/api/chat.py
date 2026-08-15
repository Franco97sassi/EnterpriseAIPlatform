from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models.analysis import TextAnalysis
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_provider import GeminiProvider


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

provider = GeminiProvider()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = await provider.generate(request.message)

        return ChatResponse(
            response=response,
            provider="gemini",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="LLM provider request failed",
        ) from exc


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    async def generate_stream():
        try:
            async for chunk in provider.stream(request.message):
                yield chunk
        except Exception:
            yield "Error while generating response."

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
    )


@router.post("/analyze", response_model=TextAnalysis)
async def analyze_text(request: ChatRequest) -> TextAnalysis:
    try:
        return await provider.analyze_text(request.message)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM structured output request failed: {exc}",
        ) from exc