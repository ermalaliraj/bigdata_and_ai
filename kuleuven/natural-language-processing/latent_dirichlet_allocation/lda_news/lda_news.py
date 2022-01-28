from pprint import pprint

import gensim
import pandas as pd
from gensim import models
# nltk.download('wordnet')
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def print_dictionary(dictionary, stop=False):
    print("\nindexed words:")
    count = 0
    for k, v in dictionary.iteritems():
        print(k, v)
        count += 1
        if count > 10 and stop:
            break


def print_tfidf(corpus_tfidf):
    print('\nbow_corpus tfidf')
    count = 0
    for doc in corpus_tfidf:
        count += 1
        pprint(doc)
        if count > 5:
            break


def lemmatize_stemming(text, stemmer):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def pre_process(text, stemmer=SnowballStemmer('english')):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token, stemmer))
    return result


def doLogic():
    data = pd.read_csv('./data/abcnews-date-text-slim.csv');
    data_text = data[['headline_text']]
    data_text['index'] = data_text.index
    documents = data_text
    print("Nr documents: ", len(documents))
    print(documents[:5])

    processed_docs = documents['headline_text'].map(pre_process)
    print("\nprocessed_docs: \n", processed_docs[:5])

    # Bag of Words on the dataset
    dictionary = Dictionary(processed_docs)
    print_dictionary(dictionary, True)

    dictionary.filter_extremes(no_below=15,  # less than 15 documents
                               no_above=0.5,  # not more than half of documents (fraction of total corpus size)
                               keep_n=100000)  # after two steps, keep only the first 100000 most frequent tokens.

    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    print("\nbow_corpus (token_id, token_count) tuples: ", *bow_corpus[:10], sep="\n")

    bow_doc_4310 = bow_corpus[4310]
    print("\nbow_doc_4310: ", bow_doc_4310)
    for i in range(len(bow_doc_4310)):
        print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0],
                                                         dictionary[bow_doc_4310[i][0]],
                                                         bow_doc_4310[i][1]))

    ## TF-IDF
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    print_tfidf(corpus_tfidf)

    # Running LDA using Bag of Words
    print('\nRunning LDA using Bag of Words')
    lda_model = LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} Words: {}'.format(idx, topic))

    # Running LDA using TF-IDF
    print('\nRunning LDA using TF-IDF')
    lda_model_tfidf = LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)
    for idx, topic in lda_model_tfidf.print_topics(-1):
        print('Topic: {} Word: {}'.format(idx, topic))

    # Classification of the topics
    # Performance evaluation by classifying sample document using LDA Bag of Words model
    print('\nprocessed_docs[4310]', processed_docs[4310])
    print('Performance evaluation by classifying LDA Bag of Words model')
    for index, score in sorted(lda_model[bow_corpus[4310]], key=lambda tup: -1 * tup[1]):
        print("Score: {}\t - Topic: {}".format(score, lda_model.print_topic(index, 10)))

    # Performance evaluation by classifying sample document using LDA TF-IDF model
    print('\nPerformance evaluation by classifying LDA TF-IDF model')
    for index, score in sorted(lda_model_tfidf[bow_corpus[4310]], key=lambda tup: -1 * tup[1]):
        print("Score: {}\t - Topic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))

    # Testing model on unseen document
    unseen_document = 'How a Pentagon deal became an identity crisis for Google'
    bow_unseen = dictionary.doc2bow(pre_process(unseen_document))
    print('\nTesting model on unseen document')
    for index, score in sorted(lda_model[bow_unseen], key=lambda tup: -1 * tup[1]):
        print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))


# needed main to avoid LdaMulticore issue
if __name__ == '__main__':
    doLogic()
