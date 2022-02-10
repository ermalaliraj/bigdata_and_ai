import pickle
import re
import xml.etree.ElementTree as ET

import gensim.corpora as corpora
import spacy
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric

year = "2017"
fileModelName = './model/lda_model_EU_REG_year-' + year + '.dat'
fileCampusName = './model/lda_model_EU_REG_year-' + year + '_campus.dat'
docPath = "../output/oj/reg_2016_679_akn.xml"

import numpy as np

np.set_printoptions(edgeitems=3, linewidth=100)


def to_string_utf8(document):
    return document.decode('utf-8')


def get_doc_data(filepath):
    tree = ET.parse(filepath)
    document = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    document = to_string_utf8(document)
    document = re.sub('[ ]+', ' ', document)
    return document


def deserializeFile(file_name):
    print("Loading ", file_name)
    with open(file_name, 'rb') as f:
        corpus = pickle.load(f)
    return corpus


def show_topics(lda_model, num_words=5):
    lda_topics_not_indexed = lda_model.show_topics(num_words=num_words, num_topics=-1)
    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
    for topic in lda_topics_not_indexed:
        # print(topic)
        topics.append(preprocess_string(topic[1], filters))
    # print(len(topics))
    print("\nTotal topics " + str(len(topics)) + ". Printing first 5:", *topics[0:5], sep='\n')
    return topics


def lemmatization(text, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    text_nlp = nlp(text)
    new_text = []
    for token in text_nlp:
        if token.pos_ in allowed_postags:
            new_text.append(token.lemma_)
    lemmatized = " ".join(new_text)
    return lemmatized


lda_model = deserializeFile(fileModelName)
corpus = deserializeFile(fileCampusName)
print("Loaded Regulations model and corpus data.")

topics = show_topics(lda_model, 5)

fileContent = get_doc_data(docPath)
fileContent = lemmatization(fileContent)

EN_STOP = ""
cats = []
documents = []

 for line in fileContent:
    if line:
        parts = line.split()
        doc = [v.strip() for v in parts[1:]]
        if not doc:
            continue
        documents.append(doc)
        cats.append(parts[0])

D = corpora.Dictionary(documents)
C = [D.doc2bow(doc) for document in documents]
# lda = fileModelName
for i, doc in enumerate(C[:4]):
    topics = lda_model[doc]
    print("topics", topics)
    estimate = max(topics, key=lambda x: x[1])
    print("document: ", doc)
    print("real topic: ", cats[i])
    print("document: ", doc)
    print("estimate topic: ", estimate)
