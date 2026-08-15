import pytest
from pydantic import ValidationError

from app.prompts.registry import get_prompt


def test_get_existing_prompt():
    prompt = get_prompt("assistant", "v1")

    assert prompt.name == "assistant"
    assert prompt.version == "1.0"
    assert prompt.system_prompt


def test_get_unknown_prompt():
    with pytest.raises(ValueError):
        get_prompt("assistant", "v999")


def test_render_user_prompt():
    prompt = get_prompt("assistant", "v1")

    rendered = prompt.render_user_prompt(
        question="What is RAG?",
        context="RAG combines retrieval with language generation.",
    )

    assert "What is RAG?" in rendered
    assert "RAG combines retrieval" in rendered


def test_render_user_prompt_missing_variable():
    prompt = get_prompt("assistant", "v1")

    with pytest.raises(ValueError, match="Missing prompt variable"):
        prompt.render_user_prompt(
            question="What is RAG?"
        )


def test_prompt_contains_few_shot_examples():
    prompt = get_prompt("assistant", "v1")

    assert len(prompt.examples) == 2
    assert prompt.examples[0].input == "What is RAG?"


def test_render_examples():
    prompt = get_prompt("assistant", "v1")

    rendered = prompt.render_examples()

    assert "User:" in rendered
    assert "Assistant:" in rendered
    assert "What is RAG?" in rendered
    assert "Retrieval-Augmented Generation" in rendered


def test_prompt_has_response_model():
    prompt = get_prompt("assistant", "v1")

    assert prompt.response_model is not None


def test_structured_response_validation():
    prompt = get_prompt("assistant", "v1")

    response = prompt.response_model(
        answer="RAG combines retrieval with generation.",
        grounded=True,
        confidence=0.95,
    )

    assert response.answer == "RAG combines retrieval with generation."
    assert response.grounded is True
    assert response.confidence == 0.95


def test_structured_response_rejects_invalid_confidence():
    prompt = get_prompt("assistant", "v1")

    with pytest.raises(ValidationError):
        prompt.response_model(
            answer="Example answer",
            grounded=True,
            confidence=1.5,
        )

def test_prompt_versions_are_independent():
    v1 = get_prompt("assistant", "v1")
    v2 = get_prompt("assistant", "v2")

    assert v1.version == "1.0"
    assert v2.version == "2.0"
    assert v1.system_prompt != v2.system_prompt


def test_prompt_rendering_is_reproducible():
    prompt = get_prompt("assistant", "v2")

    first = prompt.render_user_prompt(
        question="What is RAG?",
        context="RAG retrieves external information.",
    )

    second = prompt.render_user_prompt(
        question="What is RAG?",
        context="RAG retrieves external information.",
    )

    assert first == second