from app.prompts.models import PromptDefinition, PromptExample
from app.prompts.schemas import AssistantResponse


ASSISTANT_V2 = PromptDefinition(
    name="assistant",
    version="2.0",
    system_prompt="""
You are an enterprise AI assistant focused on grounded and verifiable answers.

Rules:
- Use available context as the primary source of truth.
- Do not fabricate facts.
- If context is insufficient, say so explicitly.
- Keep answers concise and structured.
- Distinguish clearly between known information and uncertainty.
""".strip(),
    user_template="""
Question:
{question}

Context:
{context}

Provide a grounded answer based on the context above.
""".strip(),
    examples=(
        PromptExample(
            input="What is RAG?",
            output=(
                "RAG is Retrieval-Augmented Generation, a technique that "
                "retrieves external information and supplies it as context "
                "to a language model before generating an answer."
            ),
        ),
    ),
    response_model=AssistantResponse,
    metadata={
        "purpose": "grounded_assistant",
        "language": "en",
    },
)