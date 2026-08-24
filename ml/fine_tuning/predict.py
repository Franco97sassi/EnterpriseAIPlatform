import torch

from peft import PeftModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


MODEL_NAME = "distilbert-base-uncased"
ADAPTER_PATH = "models/sentiment_lora"

ID_TO_LABEL = {
    0: "negative",
    1: "positive",
}


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        ADAPTER_PATH
    )

    base_model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
    )

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_PATH,
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

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1,
    )

    predicted_id = (
        probabilities.argmax(dim=-1).item()
    )

    confidence = probabilities[
        0,
        predicted_id,
    ].item()

    return {
        "text": text,
        "label": ID_TO_LABEL[predicted_id],
        "confidence": confidence,
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


if __name__ == "__main__":
    main()