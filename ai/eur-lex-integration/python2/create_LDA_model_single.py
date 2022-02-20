import pickle
import re
import xml.etree.ElementTree as ET
import os

import collections
import pandas as pd
import numpy as np
import spacy

import matplotlib.pyplot as plt


def to_string_utf8(document):
    return document.decode('utf-8')


def get_doc_data(filepath):
    tree = ET.parse(filepath)
    document = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    document = to_string_utf8(document)
    document = re.sub('[ \t\n]+', ' ', document)
    return document


def count_pos(text):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    doc = nlp(text)
    words_as_pos = []
    for token in doc:
        if token.is_stop == False and len(token.text) > 2:
            words_as_pos.append(token.pos_)  # POS is more about the context of the features than frequencies of features
    return " ".join(words_as_pos)


def clean(text, allowed_postags=["NOUN", "ADJ", "VERB", "ADV", "NUM"]):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    doc = nlp(text)
    cleaned_text = []
    for token in doc:
        if token.pos_ in allowed_postags and token.is_stop == False and len(token.text) > 2:
            cleaned_text.append(token.lemma_.lower())
    return " ".join(cleaned_text)


def save_content_to_file(content, filePath):
    file = open(filePath, "wb")
    pickle.dump(content, file)
    print("SAVED in ", filePath)


data_dir = "../output/oj"
year = "2019"
fileModelName = './model/lda_model_EU_REG_year-' + year + '.dat'
fileCampusName = './model/lda_model_EU_REG_year-' + year + '_campus.dat'



documents = []
for doc in os.listdir(data_dir):
    # if doc.endswith(".xml"):
    if doc.startswith("reg_" + year) and doc.endswith(".xml"):
        try:
            documents.append([doc, count_pos(get_doc_data(os.path.join(data_dir, doc)))])
        except:
            pass

fileModelName = "pos_per_documents"
documents_pos = pickle.load(open(fileModelName, "rb"))

documents = np.array(documents_pos)
all_pos = " ".join(documents[:, 1])
print("all_pos: ", all_pos[0:100], "...")

all_pos = all_pos.split()

POS_freq_counter = collections.Counter(all_pos)
print('Total number of POSs: ', len(set(POS_freq_counter)))
s_POS_freq = pd.Series(POS_freq_counter, dtype=float)
s_POS_freq = s_POS_freq.sort_values(ascending=False)
df_tmp = pd.DataFrame(s_POS_freq, columns=['Frequency'], dtype=float)
print('Total number of POSs: ', len(set(s_POS_freq)))
df_tmp.plot.bar(alpha=0.8, color='c', legend=False, title='POS frequency in all texts combined')
plt.show()

x = ["2016", "2017", "2018", "2019", "2020", "2021"]
y = [301, 284, 278, 243, 207, 272]
s_POS_freq = pd.Series(y, dtype=float)
df_tmp = pd.DataFrame(s_POS_freq, columns=['Frequency'], dtype=float)

df_tmp.plot.bar(alpha=0.8, color='c', legend=False, title='POS frequency in all texts combined')
plt.show()