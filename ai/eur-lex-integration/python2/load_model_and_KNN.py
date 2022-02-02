import pickle
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric
import numpy as np


def deserializeFile(file_name):
    print("\nLoading ", file_name)
    with open(file_name, 'rb') as f:
        corpus = pickle.load(f)
    # print("Loaded corpus: ", corpus)
    return corpus


def show_topics(lda_model, num_words=5):
    lda_topics_not_indexed = lda_model.show_topics(num_words=num_words, num_topics=-1)
    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]
    for topic in lda_topics_not_indexed:
        print(topic)
        topics.append(preprocess_string(topic[1], filters))
    # print(len(topics))
    # print(topics)
    return topics



lda_model = deserializeFile('./model/lda_books_model.dat')
corpus = deserializeFile('./model/lda_books_model_corpus.dat')
print("Loaded model and corpus data. Preparing visualisation... ")

topics = show_topics(lda_model, 5)

visualisation = gensimvis.prepare(lda_model, corpus, lda_model.id2word, mds="mmds", R=30)
pyLDAvis.save_html(visualisation, 'LDA_books_topics_visualization.html')
print("Created Visualization file: LDA_books_topics_visualization.html")

# print(len(topics))

corpus = [j for i in topics for j in i]
print(corpus)
words = corpus
corpus = " ".join(sorted(set(words), key=words.index))
import spacy

nlp = spacy.load("en_core_web_sm")
# Apply the model on our dataset of tags
tokens = nlp(corpus)

# Convert tags into vectors for our clustering model
word_vectors = []
for i in tokens:
    word_vectors.append(i.vector)
word_vectors = np.array(word_vectors)
print(word_vectors.shape)

import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
ss = StandardScaler()
X = ss.fit_transform(word_vectors)
km = KMeans(n_clusters=20)
km.fit(X)
y_pred = km.predict(X)
# print(y_pred)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='Paired')
plt.title("K-means")
plt.show()

test_words = ' '.join(['glandless', 'international', 'technology', 'program']).replace('-', ' ')
test_tokens = nlp(test_words)

test_vectors = []
for i in test_tokens:
    test_vectors.append(i.vector)
test_vectors = np.array(test_vectors)
test_pred=km.predict(test_vectors)
print("output labels : ",test_pred)



"""code to find optimal K value"""

# from sklearn.neighbors import NearestNeighbors
# neigh = NearestNeighbors(n_neighbors=2)
# nbrs = neigh.fit(word_vectors)
# distances, indices = nbrs.kneighbors(word_vectors)
# distances = np.sort(distances, axis=0)
# distances = distances[:,1]
# plt.figure(figsize=(20,10))
# plt.plot(distances)
# plt.title('K-distance Graph',fontsize=20)
# plt.xlabel('Data Points sorted by distance',fontsize=14)
# plt.ylabel('Epsilon',fontsize=14)
# plt.show()