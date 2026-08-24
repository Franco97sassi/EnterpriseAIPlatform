from transformers import AutoTokenizer


MODEL_NAME = "distilbert-base-uncased"


def main():
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    text = "The service was excellent"

    tokens = tokenizer.tokenize(text)

    token_ids = tokenizer.convert_tokens_to_ids(
        tokens
    )

    encoded = tokenizer(
        text,
        return_tensors="pt",
    )

    print("Texto:")
    print(text)

    print("\nTokens:")
    print(tokens)

    print("\nToken IDs:")
    print(token_ids)

    print("\nInput IDs del modelo:")
    print(encoded["input_ids"])

    print("\nAttention mask:")
    print(encoded["attention_mask"])


if __name__ == "__main__":
    main()