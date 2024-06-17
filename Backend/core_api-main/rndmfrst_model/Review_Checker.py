from numpy import vectorize
import pandas as pd
import string
import pickle
from pathlib import Path


def avg_word_length(text):
    words = text.split()
    return sum(len(word) for word in words) / len(words) if words else 0


def review_checker(new_text_data):
    with open(Path(__file__).parent.joinpath('review_model.pkl'), "rb") as model_file:
        loaded_model = pickle.load(model_file)

    with open(Path(__file__).parent.joinpath('vectorizer.pkl'), "rb") as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)

    new_df = pd.DataFrame({"text": new_text_data})
    new_df["text_length"] = new_df["text"].apply(len)
    new_df["word_count"] = new_df["text"].apply(lambda x: len(x.split()))
    new_df["avg_word_length"] = new_df["text"].apply(avg_word_length)
    new_df["unique_word_count"] = new_df["text"].apply(lambda x: len(set(x.split())))
    new_df["punctuation_count"] = new_df["text"].apply(
        lambda x: len([char for char in x if char in string.punctuation])
    )
    new_df["digit_count"] = new_df["text"].apply(
        lambda x: sum(char.isdigit() for char in x)
    )
    new_df["uppercase_count"] = new_df["text"].apply(
        lambda x: sum(char.isupper() for char in x)
    )
    X_new = loaded_vectorizer.transform(new_df["text"])
    predictions = loaded_model.predict(X_new)
    print("Predictions for the new text data:")
    print(predictions)
    if predictions == 0:
        return "Not Found"
    else:
        return "Found"