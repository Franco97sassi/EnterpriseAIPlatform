import joblib
import torch

from ml.deep_learning.model import SentimentNeuralNetwork


MODEL_PATH = "models/sentiment_nn.pt"
VECTORIZER_PATH = "models/sentiment_nn_vectorizer.joblib"


def load_artifacts():
    checkpoint = torch.load(
        MODEL_PATH,
        map_location="cpu",
    )

    input_size = checkpoint["input_size"]

    model = SentimentNeuralNetwork(
        input_size=input_size,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    return model, vectorizer


def predict_sentiment(text: str) -> str:
    model, vectorizer = load_artifacts()

    vectorized = vectorizer.transform(
        [text]
    )

    tensor = torch.tensor(
        vectorized.toarray(),
        dtype=torch.float32,
    )

    with torch.no_grad():
        logits = model(tensor)

        probability = torch.sigmoid(
            logits
        ).item()

    if probability >= 0.5:
        return "positive"

    return "negative"


def main():
    text = "The service was excellent"

    prediction = predict_sentiment(text)

    print("Texto:", text)
    print("Predicción:", prediction)


if __name__ == "__main__":
    main()