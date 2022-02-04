import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# for text preprocessing
import re
import spacy

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

# import vectorizers
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# import numpy for matrix operation
import numpy as np

# import LDA from sklearn
from sklearn.decomposition import LatentDirichletAllocation
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

def byte_to_string(document):
    return document.decode('utf-8')

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


tree = ET.parse('../resources/reg_2013_1303_akn.xml')


documents = ET.tostringlist(tree.getroot(), encoding='utf-8', method='text')
documents = list(map(byte_to_string, documents))
print("Total document", len(documents))


stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
print("stop ", stop)
print("exclude ", exclude)
print("lemma ", lemma)

doc = documents[0]
stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
print("doc ", doc)
print("stop_free {}, {}", len(stop_free), stop_free)
print("punc_free  {}, {}", len(punc_free), punc_free)
print("normalized  {}, {}", len(normalized), normalized)
# print("doc2 ", normalized)

# clean_corpus = [list(set(clean(doc).split())) for doc in documents]
#
# print("clean_corpus", clean_corpus)