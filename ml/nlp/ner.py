import nltk

from nltk import ne_chunk
from nltk.tag import pos_tag

from ml.nlp.tokenize import tokenize_text


def extract_entities(text: str):
    tokens = tokenize_text(text)

    tagged_tokens = pos_tag(tokens)

    entity_tree = ne_chunk(
        tagged_tokens
    )

    entities = []

    for node in entity_tree:
        if hasattr(node, "label"):
            entity = " ".join(
                word
                for word, _ in node.leaves()
            )

            entities.append(
                {
                    "text": entity,
                    "label": node.label(),
                }
            )

    return entities


def main():
    text = (
        "Barack Obama worked in Washington "
        "and visited Microsoft."
    )

    entities = extract_entities(text)

    print("Texto:")
    print(text)

    print("\nEntidades encontradas:")

    for entity in entities:
        print(
            f'{entity["text"]} -> '
            f'{entity["label"]}'
        )


if __name__ == "__main__":
    main()