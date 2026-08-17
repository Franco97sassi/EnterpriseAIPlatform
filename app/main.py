from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.agents.router import router as agents_router


app = FastAPI(
    title="Enterprise AI Platform",
    description="Enterprise AI Engineering platform built with Python.",
    version="0.1.0",
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(chat_router)
app.include_router(agents_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "enterprise-ai-platform",
    }