import pickle

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt


def clean(text):
    lemmatizer = WordNetLemmatizer()
    stopwordList = set(stopwords.words("english"))
    words = text.lower().split(" ")
    cleaned_text = ""
    for word in words:
        if word in stopwordList: continue
        cleaned_text += lemmatizer.lemmatize(word) + " "

    return cleaned_text


path = "../output/oj"
year = "2016"
fileModelName = './model/lda_model_EU_REG_year-' + year + '.pkl'
fileTopicsName = './model/lda_model_EU_REG_year-' + year + '_topics.pkl'
fileTopicToDocumentName = './model/lda_model_EU_REG_year-' + year + '_topic_to_document.pkl'

print("Loading Model and Metadata...")
model = pickle.load(open(fileModelName, "rb"))
topics = pickle.load(open(fileTopicsName, "rb"))
topic_to_document = pickle.load(open(fileTopicToDocumentName, "rb"))


text = input("Enter text: ")

pred = np.argmax(model.predict([clean(text)]))
print("Topic ->", topics[pred])
print("Similar Documents ->", topic_to_document[pred])
