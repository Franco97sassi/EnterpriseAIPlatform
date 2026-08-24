from ml.fine_tuning.predict import predict_sentiment


def test_lora_prediction_returns_valid_result():
    result = predict_sentiment(
        "The service was excellent"
    )

    assert result["label"] in {
        "positive",
        "negative",
    }

    assert 0.0 <= result["confidence"] <= 1.0