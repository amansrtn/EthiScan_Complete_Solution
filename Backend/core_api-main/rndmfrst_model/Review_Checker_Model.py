import numpy as np
import pandas as pd
import string
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from lightgbm import LGBMClassifier


def avg_word_length(text):
    words = text.split()
    return sum(len(word) for word in words) / len(words) if words else 0


df_essay = pd.read_csv("train_essays.csv")

df_essay["text_length"] = df_essay["text"].apply(len)
df_essay["word_count"] = df_essay["text"].apply(lambda x: len(x.split()))
df_essay["avg_word_length"] = df_essay["text"].apply(avg_word_length)
df_essay["unique_word_count"] = df_essay["text"].apply(lambda x: len(set(x.split())))
df_essay["punctuation_count"] = df_essay["text"].apply(
    lambda x: len([char for char in x if char in string.punctuation])
)
df_essay["digit_count"] = df_essay["text"].apply(
    lambda x: sum(char.isdigit() for char in x)
)
df_essay["uppercase_count"] = df_essay["text"].apply(
    lambda x: sum(char.isupper() for char in x)
)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X_train = vectorizer.fit_transform(df_essay["text"])

# Prepare target
y_train = df_essay["generated"]

# Model Training
model = LGBMClassifier(n_estimators=1000, learning_rate=0.05, num_leaves=31)
model.fit(X_train, y_train)

# Save the model as a pickle file
with open("review_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
