import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from ml.transformers.inference import predict_sentiment


DATASET_PATH = "data/sentiment.csv"


def main():
    df = pd.read_csv(DATASET_PATH)

    real_labels = []
    predicted_labels = []

    for _, row in df.iterrows():
        text = row["text"]
        real_label = row["label"]

        result = predict_sentiment(text)

        predicted_label = result["label"].lower()

        real_labels.append(real_label)
        predicted_labels.append(predicted_label)

        print(
            f"{text} -> "
            f"Real: {real_label} | "
            f"Predicción: {predicted_label}"
        )

    accuracy = accuracy_score(
        real_labels,
        predicted_labels,
    )

    precision = precision_score(
        real_labels,
        predicted_labels,
        pos_label="positive",
        zero_division=0,
    )

    recall = recall_score(
        real_labels,
        predicted_labels,
        pos_label="positive",
        zero_division=0,
    )

    f1 = f1_score(
        real_labels,
        predicted_labels,
        pos_label="positive",
        zero_division=0,
    )

    print("\nMétricas Transformer:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")


if __name__ == "__main__":
    main()