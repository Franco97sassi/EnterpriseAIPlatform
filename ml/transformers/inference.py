import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


MODEL_NAME = (
    "distilbert-base-uncased-finetuned-sst-2-english"
)


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME
    )

    model.eval()

    return tokenizer, model


def predict_sentiment(text: str):
    tokenizer, model = load_model()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    probabilities = torch.softmax(
        logits,
        dim=-1,
    )

    predicted_class_id = (
        probabilities.argmax(dim=-1).item()
    )

    predicted_label = model.config.id2label[
        predicted_class_id
    ]

    confidence = probabilities[
        0,
        predicted_class_id,
    ].item()

    return {
        "text": text,
        "label": predicted_label,
        "confidence": confidence,
        "logits": logits.tolist(),
        "probabilities": probabilities.tolist(),
    }


def main():
    text = "The service was excellent"

    result = predict_sentiment(text)

    print("Texto:")
    print(result["text"])

    print("\nPredicción:")
    print(result["label"])

    print("\nConfianza:")
    print(f'{result["confidence"]:.4f}')

    print("\nProbabilidades:")
    print(result["probabilities"])


if __name__ == "__main__":
    main()