import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


DATASET_PATH = "data/sentiment.csv"


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def split_dataset(df: pd.DataFrame):
    X = df["text"]
    y = df["label"]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )


def main():
    df = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(df)

    vectorizer = TfidfVectorizer()

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    model = LogisticRegression()

    model.fit(
        X_train_vectorized,
        y_train,
    )


    joblib.dump(
    model,
    "models/sentiment_model.joblib",
)

    joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.joblib",
    )

    print("\nModelo guardado correctamente.")
    predictions = model.predict(X_test_vectorized)

    print("Predicciones:")

    for text, real, predicted in zip(X_test, y_test, predictions):
        print(f"\nTexto: {text}")
        print(f"Real: {real}")
        print(f"Predicción: {predicted}")

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        pos_label="positive",
    )

    recall = recall_score(
        y_test,
        predictions,
        pos_label="positive",
    )

    f1 = f1_score(
        y_test,
        predictions,
        pos_label="positive",
    )

    print("\nMétricas:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

    print("\nInformación del modelo:")
    print("Cantidad de ejemplos de entrenamiento:", X_train_vectorized.shape[0])
    print("Cantidad de features:", X_train_vectorized.shape[1])

    print("\nAlgunas palabras del vocabulario:")
    print(vectorizer.get_feature_names_out()[:20])


if __name__ == "__main__":
    main()