from fastapi import FastAPI

from app.api.chat import router as chat_router


app = FastAPI(
    title="Enterprise AI Platform",
    description="Enterprise AI Engineering platform built with Python.",
    version="0.1.0",
)

app.include_router(chat_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "enterprise-ai-platform",
    }