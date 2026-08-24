import pandas as pd

from datasets import Dataset


DATASET_PATH = "data/sentiment.csv"

LABEL_TO_ID = {
    "negative": 0,
    "positive": 1,
}


def prepare_dataset():
    df = pd.read_csv(DATASET_PATH)

    df["label"] = df["label"].map(
        LABEL_TO_ID
    )

    dataset = Dataset.from_pandas(
        df,
        preserve_index=False,
    )

    split_dataset = dataset.train_test_split(
        test_size=0.2,
        seed=42,
    )

    return split_dataset


def main():
    dataset = prepare_dataset()

    print("Dataset:")
    print(dataset)

    print("\nEntrenamiento:")
    print(dataset["train"])

    print("\nTest:")
    print(dataset["test"])

    print("\nPrimer ejemplo:")
    print(dataset["train"][0])


if __name__ == "__main__":
    main()