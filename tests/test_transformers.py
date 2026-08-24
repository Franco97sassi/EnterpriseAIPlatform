from ml.transformers.inference import predict_sentiment


def test_transformer_prediction_returns_valid_result():
    result = predict_sentiment(
        "The service was excellent"
    )

    assert result["label"] in {
        "POSITIVE",
        "NEGATIVE",
    }

    assert 0.0 <= result["confidence"] <= 1.0