from ml.deep_learning.predict import predict_sentiment


def test_deep_learning_prediction_returns_valid_label():
    result = predict_sentiment(
        "The service was excellent"
    )

    assert result in {
        "positive",
        "negative",
    }