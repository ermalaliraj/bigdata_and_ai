import re
import re
import xml.etree.ElementTree as ET

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

docPath = '../resources/reg_2013_1303_akn.xml'


def to_string_utf8(docContent):
    return docContent.decode('utf-8')


def get_doc_content(filepath):
    tree = ET.parse(filepath)
    docContent = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    docContent = to_string_utf8(docContent)
    pasttern = '[ \t\n]+'
    docContent = re.sub(pasttern, ' ', docContent)
    return docContent


def lemmatizeWithSpacyModel(text, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    # nlp = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
    nlp_model = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    nlp = nlp_model(text)
    new_text = []
    for token in nlp:
        if allowed_postags is not None:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        else:
            new_text.append(token.lemma_)
    normalized_text = " ".join(new_text)
    return normalized_text


def lemmatize(text):
    stop = stopwords.words('english')  # 461713   332127
    exclude = [',', '!', '^', '$', '[', ']', ':', '<', "'", '@', '=', '}', '-', '?', '~', '+', '|', '(', '`', '#', ';',
               '>', '_', '{', '\\', ')', '*', '%', '"', '&']
    # print("stop ", stop)
    # print("exclude ", exclude)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in text.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def stemming(text):
    stemmer = nltk.porter.PorterStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


docContent = get_doc_content(docPath)
print("docContent                   ({}):{}".format(len(docContent), docContent))

lemmatize_str = lemmatize(docContent)
print("lemmatize_str                ({}):{}".format(len(lemmatize_str), lemmatize_str))

stemming_str = stemming(docContent)
print("stemming_str                 ({}):{}".format(len(stemming_str), stemming_str))

lemmatize_stemming_str = lemmatize(stemming(docContent))
print("lemmatize_stemming_str       ({}):{}".format(len(lemmatize_stemming_str), lemmatize_stemming_str))

# lemmatizedWithSpacyModel = lemmatizeWithSpacyModel(docContent, None)
# print("lemmatizedWithSpacyModel all ({}):{}".format(len(lemmatizedWithSpacyModel), lemmatizedWithSpacyModel))
# lemmatizedWithSpacyModel = lemmatizeWithSpacyModel(docContent)
# print("lemmatizedWithSpacyModel     ({}):{}".format(len(lemmatizedWithSpacyModel), lemmatizedWithSpacyModel))
