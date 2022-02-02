import pickle

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric

def deserializeFile(file_name):
    print("\nLoading ", file_name)
    with open(file_name, 'rb') as f:
        corpus = pickle.load(f)
    print("Loaded corpus: ", corpus)
    return corpus


def show_topics(lda_model, num_words=5):
    lda_topics_not_indexed = lda_model.show_topics(num_words=num_words)
    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
    for topic in lda_topics_not_indexed:
        print(topic)
        topics.append(preprocess_string(topic[1], filters))
    print("topics", *topics, sep='\n')
    # lda_topics_indexed = lda_model.show_topics(formatted=False, num_words=5)
    # for index, topic in lda_topics_indexed:
    #     print('Topic: {} \nWords: {}'.format(index, [w[0] for w in topic]))


lda_model = deserializeFile('./model/lda_books_model.dat')
corpus = deserializeFile('./model/lda_eu_regulations_model_corpus.dat')
print("Loaded model and corpus data. Preparing visualisation... ")

show_topics(lda_model, 5)

visualisation = gensimvis.prepare(lda_model, corpus, lda_model.id2word, mds="mmds", R=30)
pyLDAvis.save_html(visualisation, 'LDA_books_topics_visualization.html')
print("Created Visualization file: LDA_books_topics_visualization.html")