from ml.classical.predict import predict_sentiment


def test_predict_sentiment_returns_valid_label():
    result = predict_sentiment(
        "The service was excellent"
    )

    assert result in {
        "positive",
        "negative",
    }