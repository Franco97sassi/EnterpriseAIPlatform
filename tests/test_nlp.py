from ml.nlp.preprocess import (
    normalize_text,
    stem_tokens,
    lemmatize_tokens,
)
from ml.nlp.ner import extract_entities


def test_normalize_text():
    result = normalize_text(
        "The SERVICE was Excellent!!!"
    )

    assert result == "the service was excellent"


def test_stemming():
    result = stem_tokens(
        ["programming", "applications"]
    )

    assert len(result) == 2
    assert result[0] == "program"


def test_lemmatization():
    result = lemmatize_tokens(
        ["applications"]
    )

    assert result == ["application"]


def test_ner_returns_entities():
    result = extract_entities(
        "Barack Obama worked in Washington."
    )

    assert len(result) > 0

    assert all(
        "text" in entity and "label" in entity
        for entity in result
    )