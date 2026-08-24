import nltk

from nltk.tokenize import word_tokenize


def tokenize_text(text: str) -> list[str]:
    return word_tokenize(text)


def main():
    nltk.download(
        "punkt_tab",
        quiet=True,
    )

    text = "The service was excellent and very fast."

    tokens = tokenize_text(text)

    print("Texto:")
    print(text)

    print("\nTokens:")
    print(tokens)

    print("\nCantidad de tokens:")
    print(len(tokens))


if __name__ == "__main__":
    main()