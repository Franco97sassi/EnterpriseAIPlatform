import joblib


MODEL_PATH = "models/sentiment_model.joblib"
VECTORIZER_PATH = "models/tfidf_vectorizer.joblib"


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return model, vectorizer


def predict_sentiment(text: str) -> str:
    model, vectorizer = load_artifacts()

    text_vectorized = vectorizer.transform([text])

    prediction = model.predict(text_vectorized)[0]

    return prediction


def main():
    text = "The service was excellent"

    prediction = predict_sentiment(text)

    print("Texto:", text)
    print("Predicción:", prediction)


if __name__ == "__main__":
    main()