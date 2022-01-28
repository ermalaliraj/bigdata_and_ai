import json
import pickle
import warnings

import gensim
import gensim.corpora as corpora
import spacy

spacy.load('en_core_web_sm')
from nltk.corpus import stopwords

warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


stopwords = stopwords.words("english")
print("\nstopwords: ", stopwords)

data = load_data("data/ushmm_dn.json")["texts"]
print("\ndata size: ", len(data))
print("data[0][0:90]: ", data[0][0:90])


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


lemmatized_texts = lemmatization(data)
print("\nlemmatized_texts size: ", len(lemmatized_texts))
print("lemmatized_texts[0][0:90]: ", lemmatized_texts[0][0:90])


def gen_words(texts):
    final = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final


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

outputFile = open('./model/lda_books_model_corpus.dat', 'wb')
pickle.dump(corpus, outputFile)
outputFile.close()
print("Corpus data saved in: ", outputFile.name)

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=30,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha="auto")

with open('./model/lda_books_model.dat', 'wb') as f:
    pickle.dump(lda_model, f)
print("Model saved in: ", f.name)
