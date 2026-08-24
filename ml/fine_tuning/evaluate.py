import torch

from peft import PeftModel
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from ml.fine_tuning.prepare_dataset import prepare_dataset


MODEL_NAME = "distilbert-base-uncased"
ADAPTER_PATH = "models/sentiment_lora"


def main():
    # =========================
    # DATASET
    # =========================

    dataset = prepare_dataset()

    test_dataset = dataset["test"]

    # =========================
    # TOKENIZER
    # =========================

    tokenizer = AutoTokenizer.from_pretrained(
        ADAPTER_PATH
    )

    # =========================
    # MODELO BASE
    # =========================

    base_model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
    )

    # =========================
    # CARGAR ADAPTER LoRA
    # =========================

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_PATH,
    )

    model.eval()

    real_labels = []
    predicted_labels = []

    # =========================
    # PREDICCIONES
    # =========================

    for example in test_dataset:
        text = example["text"]
        real_label = example["label"]

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
        )

        with torch.no_grad():
            outputs = model(**inputs)

        prediction = (
            outputs.logits
            .argmax(dim=-1)
            .item()
        )

        real_labels.append(real_label)
        predicted_labels.append(prediction)

        print(
            f"{text} -> "
            f"Real: {real_label} | "
            f"Predicción: {prediction}"
        )

    # =========================
    # MÉTRICAS
    # =========================

    accuracy = accuracy_score(
        real_labels,
        predicted_labels,
    )

    precision = precision_score(
        real_labels,
        predicted_labels,
        zero_division=0,
    )

    recall = recall_score(
        real_labels,
        predicted_labels,
        zero_division=0,
    )

    f1 = f1_score(
        real_labels,
        predicted_labels,
        zero_division=0,
    )

    print("\nMétricas LoRA:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")


if __name__ == "__main__":
    main()