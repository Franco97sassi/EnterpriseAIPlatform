from collections.abc import AsyncIterator

from google import genai

from app.core.config import settings
from app.models.analysis import TextAnalysis
from app.services.llm_provider import LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    async def generate(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text or ""

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        response = await self.client.aio.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def analyze_text(self, text: str) -> TextAnalysis:
        response = await self.client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze the following text:\n\n{text}",
            config={
                "response_mime_type": "application/json",
                "response_schema": TextAnalysis,
            },
        )

        return TextAnalysis.model_validate_json(response.text)