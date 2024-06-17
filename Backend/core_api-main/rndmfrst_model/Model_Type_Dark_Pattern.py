import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
import string
from textblob import TextBlob
from nltk.corpus import stopwords


df = pd.read_csv("dark-patterns-new2.csv")

df.dropna(subset=["Pattern String"], inplace=True)

exclude = string.punctuation


def rempun(text):
    return text.translate(str.maketrans("", "", exclude))


# spelling correction
# def spellcorr(text):
#     return TextBlob(text).correct().string


# removing stopwords
def remstop(text):
    newtext = []
    for w in text.split():
        if w in stopwords.words("english"):
            newtext.append("")
        else:
            newtext.append(w)
    x = newtext[:]
    newtext.clear()
    return " ".join(x)


# lowercasing
df["Pattern String"] = df["Pattern String"].str.lower()

df["Pattern String"] = df["Pattern String"].apply(rempun)

# df["Pattern String"] = df["Pattern String"].apply(spellcorr)


df["Pattern String"] = df["Pattern String"].apply(remstop)

x = df.drop(columns=["Pattern Type"])
y = df["Pattern Type"]

from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

y = encoder.fit_transform(y)

encoder.classes_

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()
X_train_tfidf = tfidf.fit_transform(X_train["Pattern String"]).toarray()
X_test_tfidf = tfidf.transform(X_test["Pattern String"])

pickle.dump(tfidf, open("tfidf_vectorizer.pkl", "wb"))

rf = RandomForestClassifier()

rf.fit(X_train_tfidf, y_train)
y_pred = rf.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


pickle.dump(rf, open("model.pkl", "wb"))
model = pickle.load(open("model.pkl", "rb"))
print(encoder.classes_)
