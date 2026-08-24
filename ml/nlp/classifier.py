import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ml.nlp.preprocess import normalize_text


DATASET_PATH = "data/sentiment.csv"


def main():
    df = pd.read_csv(DATASET_PATH)

    df["text"] = df["text"].apply(
        normalize_text
    )

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    # Importamos acá para mantener visible
    # cada etapa del pipeline.
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer()

    X_train_features = vectorizer.fit_transform(
        X_train
    )

    X_test_features = vectorizer.transform(
        X_test
    )

    classifier = LogisticRegression()

    classifier.fit(
        X_train_features,
        y_train,
    )

    predictions = classifier.predict(
        X_test_features
    )

    print("Predicciones:")

    for text, real, predicted in zip(
        X_test,
        y_test,
        predictions,
    ):
        print(
            f"{text} -> "
            f"Real: {real} | "
            f"Predicción: {predicted}"
        )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    print("\nAccuracy:")
    print(f"{accuracy:.2f}")


if __name__ == "__main__":
    main()