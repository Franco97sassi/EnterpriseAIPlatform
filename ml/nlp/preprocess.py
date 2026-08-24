import re

import nltk

from nltk.stem import (
    PorterStemmer,
    WordNetLemmatizer,
)

from ml.nlp.tokenize import tokenize_text


# =========================
# NORMALIZACIÓN
# =========================

def normalize_text(text: str) -> str:
    # Convertir a minúsculas
    text = text.lower()

    # Eliminar caracteres que no sean letras o espacios
    text = re.sub(
        r"[^a-z\s]",
        "",
        text,
    )

    # Eliminar espacios duplicados
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# =========================
# STEMMING
# =========================

def stem_tokens(tokens: list[str]) -> list[str]:
    stemmer = PorterStemmer()

    return [
        stemmer.stem(token)
        for token in tokens
    ]


# =========================
# LEMMATIZATION
# =========================

def lemmatize_tokens(tokens: list[str]) -> list[str]:
    lemmatizer = WordNetLemmatizer()

    return [
        lemmatizer.lemmatize(token)
        for token in tokens
    ]


# =========================
# DEMO
# =========================

def main():
    nltk.download(
        "wordnet",
        quiet=True,
    )

    text = "The programmers are programming applications"

    normalized = normalize_text(text)

    tokens = tokenize_text(
        normalized
    )

    stems = stem_tokens(
        tokens
    )

    lemmas = lemmatize_tokens(
        tokens
    )

    print("Texto original:")
    print(text)

    print("\nTexto normalizado:")
    print(normalized)

    print("\nTokens:")
    print(tokens)

    print("\nStemming:")
    print(stems)

    print("\nLemmatization:")
    print(lemmas)


if __name__ == "__main__":
    main()