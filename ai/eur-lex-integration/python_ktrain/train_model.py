import os
import pickle
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

import ktrain
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')


def to_string_utf8(document):
    return document.decode('utf-8')


def get_doc_data(filepath):
    tree = ET.parse(filepath)
    document = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    document = to_string_utf8(document)
    document = re.sub('[ \t\n]+', ' ', document)
    return document


def clean(text):
    lemmatizer = WordNetLemmatizer()
    stopwordList = set(stopwords.words("english"))
    words = text.lower().split(" ")
    cleaned_text = ""
    for word in words:
        if word in stopwordList:
            continue
        cleaned_text += lemmatizer.lemmatize(word) + " "

    return cleaned_text


def save_content_to_file(content, filePath):
    file = open(filePath, "wb")
    pickle.dump(content, file)
    print("SAVED in ", filePath)


path = "../output/oj"
year = "2016"
fileModelName = './model/lda_model_EU_REG_year-' + year + '.pkl'
fileTopicsName = './model/lda_model_EU_REG_year-' + year + '_topics.pkl'
fileTopicToDocumentName = './model/lda_model_EU_REG_year-' + year + '_topic_to_document.pkl'
fileVisualization = './model/lda_model_EU_REG_year-' + year + '_topics_visualisation.html'

documents = []
for doc in os.listdir(path):
    if doc.endswith(".xml"):
        # if doc.startswith("reg_" + year) and doc.endswith(".xml"):
        try:
            documents.append([doc, clean(get_doc_data(os.path.join(path, doc)))])
        except:
            pass

documents = np.array(documents)
print("Building the model based on {} regulations".format(len(documents)))

model = ktrain.text.get_topic_model(documents[:, 1], n_topics=None, n_features=10000)
model.build(documents[:, 1], threshold=0.25)
topics = model.get_topics()
print("Total topics: ", len(topics))

save_content_to_file(model, fileModelName)
save_content_to_file(topics, fileTopicsName)

print("\nAll Topics (topicId | nrOfDocumentsTalkingAboutThisTopic | distributionOfWordsForTheTopic): ")
model.print_topics(show_counts=True)

topic_to_document = defaultdict(list)
for i in documents:
    pred = model.predict([i[1]])
    topic_to_document[np.argmax(pred)].append(i[0])
save_content_to_file(topic_to_document, fileTopicToDocumentName)

print("\nList of Documents for each Topic: (5)")
for key, value in topic_to_document.items():
    print("Topic {} - Documents list: {}".format(key, value[:5]))

print("\nSaving visualization file to :", fileVisualization)
model.visualize_documents(doc_topics=model.get_doctopics(), filepath=fileVisualization)
