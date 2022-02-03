import os
import pickle
import re
import xml.etree.ElementTree as ET

import gensim
import gensim.corpora as corpora
import spacy

data_dir = "../output/oj"
year = "2016-17-18-19-20-21"
fileModelName = './model/lda_model_EU_REG_year-' + year + '.dat'
fileCampusName = './model/lda_model_EU_REG_year-' + year + '_campus.dat'


def to_string_utf8(document):
    return document.decode('utf-8')


def get_doc_data(filepath):
    tree = ET.parse(filepath)
    document = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    document = to_string_utf8(document)
    document = re.sub('[ \t\n]+', ' ', document)
    return document


def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    texts_out = []
    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out


def gen_words(texts):
    final = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final


docs = []
for filename in os.listdir(data_dir):
    # if filename.startswith("reg_" + year) and filename.endswith(".xml"):
    if filename.endswith(".xml"):
        try:
            docs.append(get_doc_data(os.path.join(data_dir, filename)))
        except:
            pass
            # print(os.path.join(data_dir, x))

print("Total number of documents : -", len(docs))
print("doc[0] - ", docs[0][0: 150], "...")
print("doc[1] - ", docs[1][0: 150], "...")
print("doc[2] - ", docs[2][0: 150], "...")
print("doc[3] - ", docs[3][0: 150], "...")
print("doc[4] - ", docs[4][0: 150], "...")

lemmatized_texts = lemmatization(docs)
print("\nlemmatized_texts size: ", len(lemmatized_texts))
print("lemmatized_texts[0][0:90]: ", lemmatized_texts[0][0:90])

data_words = gen_words(lemmatized_texts)
print("\ndata_words size: ", len(data_words))
print("data_words[0][0:20]: ", data_words[0][0:20])

id2word = corpora.Dictionary(data_words)
print("\nid2word size: ", len(id2word))
print("id2word[[0][:1][0]]: ", id2word[[0][:1][0]])

corpus = []
for text in data_words:
    new = id2word.doc2bow(text)
    corpus.append(new)
print("\ncorpus size: ", len(corpus))
print("corpus[0][0:20]: ", corpus[0][0:20])

outputFile = open(fileCampusName, 'wb')
pickle.dump(corpus, outputFile)
outputFile.close()
print("Corpus data saved in: ", outputFile.name)

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=100,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha="auto")

with open(fileModelName, 'wb') as f:
    pickle.dump(lda_model, f)
print("Model saved in: ", f.name)

print("print_topics(-1): ", lda_model.print_topics(-1))
print("show_topics(): ", lda_model.show_topics())
