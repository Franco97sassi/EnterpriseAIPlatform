from sklearn.feature_extraction.text import TfidfVectorizer

from ml.nlp.preprocess import normalize_text


def create_tfidf_features(texts: list[str]):
    normalized_texts = [
        normalize_text(text)
        for text in texts
    ]

    vectorizer = TfidfVectorizer()

    features = vectorizer.fit_transform(
        normalized_texts
    )

    return vectorizer, features


def main():
    texts = [
        "The service was excellent",
        "The service was terrible",
        "The application works perfectly",
        "The application crashes constantly",
    ]

    vectorizer, features = create_tfidf_features(
        texts
    )

    print("Vocabulario:")
    print(vectorizer.get_feature_names_out())

    print("\nShape:")
    print(features.shape)

    print("\nMatriz TF-IDF:")
    print(features.toarray())


if __name__ == "__main__":
    main()