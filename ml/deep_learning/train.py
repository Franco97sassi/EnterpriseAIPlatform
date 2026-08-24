import pandas as pd
import torch
import joblib

from torch import nn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from ml.deep_learning.model import SentimentNeuralNetwork


DATASET_PATH = "data/sentiment.csv"


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def main():
    df = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    vectorizer = TfidfVectorizer()

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    X_train_tensor = torch.tensor(
        X_train_vectorized.toarray(),
        dtype=torch.float32,
    )

    X_test_tensor = torch.tensor(
        X_test_vectorized.toarray(),
        dtype=torch.float32,
    )

    y_train_tensor = torch.tensor(
        [1.0 if label == "positive" else 0.0 for label in y_train],
        dtype=torch.float32,
    ).reshape(-1, 1)

    y_test_tensor = torch.tensor(
        [1.0 if label == "positive" else 0.0 for label in y_test],
        dtype=torch.float32,
    ).reshape(-1, 1)

    input_size = X_train_tensor.shape[1]

    model = SentimentNeuralNetwork(
        input_size=input_size,
    )

    loss_function = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.01,
    )

    epochs = 100

    # =========================
    # ENTRENAMIENTO
    # =========================

    model.train()

    for epoch in range(epochs):
        logits = model(X_train_tensor)

        loss = loss_function(
            logits,
            y_train_tensor,
        )

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(
                f"Epoch {epoch + 1}/{epochs} "
                f"- Loss: {loss.item():.4f}"
            )

    # =========================
    # EVALUACIÓN
    # =========================

    model.eval()

    with torch.no_grad():
        test_logits = model(X_test_tensor)

        probabilities = torch.sigmoid(
            test_logits
        )

        predictions = (
            probabilities >= 0.5
        ).float()

    y_test_numpy = (
        y_test_tensor
        .numpy()
        .flatten()
    )

    predictions_numpy = (
        predictions
        .numpy()
        .flatten()
    )

    accuracy = accuracy_score(
        y_test_numpy,
        predictions_numpy,
    )

    precision = precision_score(
        y_test_numpy,
        predictions_numpy,
        zero_division=0,
    )

    recall = recall_score(
        y_test_numpy,
        predictions_numpy,
        zero_division=0,
    )

    f1 = f1_score(
        y_test_numpy,
        predictions_numpy,
        zero_division=0,
    )

    print("\nMétricas de test:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

    print("\nX train:", X_train_tensor.shape)
    print("y train:", y_train_tensor.shape)

    print("\nX test:", X_test_tensor.shape)
    print("y test:", y_test_tensor.shape)

    print("\nCantidad de features:", input_size)

    print("\nModelo:")
    print(model)

    # =========================
    # GUARDAR MODELO
    # =========================

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "input_size": input_size,
        },
        "models/sentiment_nn.pt",
    )

    joblib.dump(
        vectorizer,
        "models/sentiment_nn_vectorizer.joblib",
    )

    print("\nModelo Deep Learning guardado correctamente.")


if __name__ == "__main__":
    main()