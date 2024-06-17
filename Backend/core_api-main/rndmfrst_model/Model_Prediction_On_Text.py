import pickle
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from pathlib import Path



def Predict_Dark_Pattern_Type(new_text):
    model = pickle.load(open(Path(__file__).parent.joinpath('model.pkl'), "rb"))

    tfidf_vectorizer = pickle.load(open(Path(__file__).parent.joinpath("tfidf_vectorizer.pkl"), "rb"))

    DarkPatternType = ['Activity Notification', 'Clean', 'Confirmshaming', 'Countdown Timer',
 'Forced Enrollment', 'Hard to Cancel', 'High-demand Message',
 'Limited-time Message', 'Low-stock Message', 'Pressured Selling',
 'Sneak into Basket', 'Visual Interference']
    exclude = string.punctuation

    def rempun(text):
        return text.translate(str.maketrans("", "", exclude))

    def spellcorr(text):
        return TextBlob(text).correct().string

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

    new_text = new_text.lower()
    new_text = rempun(new_text)
    new_text = spellcorr(new_text)
    new_text = remstop(new_text)

    X_new_text_tfidf = tfidf_vectorizer.transform([new_text]).toarray()

    predicted_value = model.predict(X_new_text_tfidf)
    predicted_val = model.predict_proba(X_new_text_tfidf)
    # print(f" score is {predicted_val[0]}")
    # print(f" value is {predicted_value[0]}")
    if(predicted_val[0][1]>.30 or predicted_val[0][predicted_value[0]] < 0.4):
        return DarkPatternType[1]
    # print(new_text,"Predicted Pattern Type:", DarkPatternType[predicted_value[0]])
    return DarkPatternType[predicted_value[0]]
