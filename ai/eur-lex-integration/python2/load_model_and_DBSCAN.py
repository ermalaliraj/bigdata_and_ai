import pickle

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import spacy
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric
from sklearn.cluster import DBSCAN


def deserializeFile(file_name):
    print("\nLoading ", file_name)
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


def tag_to_vector(tokens):
    word_vectors = []
    for i in tokens:
        word_vectors.append(i.vector)
    word_vectors = np.array(word_vectors)
    return word_vectors


lda_model = deserializeFile('./model/lda_books_model.dat')
corpus = deserializeFile('./model/lda_books_model_corpus.dat')
print("Loaded Regulations model and corpus data.")

topics = show_topics(lda_model, 5)

print("Preparing visualisation... ")
visualisation = gensimvis.prepare(lda_model, corpus, lda_model.id2word, mds="mmds", R=30)
pyLDAvis.save_html(visualisation, 'LDA_Regulation_topics.html')
print("Created Visualization file: LDA_Regulation_topics.html")

print("\nChecking {} topics loaded from the model".format(len(topics)))
corpus = [j for i in topics for j in i]
print("Total words in topics ", len(corpus))
words = corpus
corpus = " ".join(sorted(set(words), key=words.index))
print("Re-build corpus string concatenating all {} words sorted by words.index".format(len(corpus)))

nlp = spacy.load("en_core_web_sm")
tokens = nlp(corpus)
print("Generated {} tokens".format(len(tokens)))

# Convert tags into vectors for our clustering model
word_vectors = tag_to_vector(tokens)
print("word_vectors from tokens", word_vectors.shape)

print("\nPerform DBSCAN clustering from vector array or distance matrix. :- ")

# Use cosine because spacy uses cosine. min_samples = 2 because a cluster should have atleast 2 similar words
dbscan = DBSCAN(metric='cosine', eps=0.3, min_samples=5).fit(word_vectors)
print("DBSCAN labels with the word_vectors: \n", dbscan.labels_)


def dbscan_predict(model, X):
    nr_samples = X.shape[0]
    y_new = np.ones(shape=nr_samples, dtype=int) * -1
    for i in range(nr_samples):
        diff = model.components_ - X[i, :]  # NumPy broadcasting
        dist = np.linalg.norm(diff, axis=1)  # Euclidean distance
        shortest_dist_idx = np.argmin(dist)
        if dist[shortest_dist_idx] < model.eps:
            y_new[i] = model.labels_[model.core_sample_indices_[shortest_dist_idx]]
    return y_new


test_words = ' '.join(['glandless', 'international', 'technology', 'program']).replace('-', ' ')
test_tokens = nlp(test_words)
test_vectors = tag_to_vector(test_tokens)
print("\ntest_tokens: ", test_tokens)
print("test_vectors from test_tokens[4x9] instead of 229x96\n", test_vectors[0:4, 0:5])

print("\nSome predictions")
print('Label for glandless:' + str(dbscan_predict(dbscan, np.array([test_vectors[0]]))[0]))
print('Label for international:' + str(dbscan_predict(dbscan, np.array([test_vectors[1]]))[0]))
print('Label for technology:' + str(dbscan_predict(dbscan, np.array([test_vectors[2]]))[0]))
print('Label for program:' + str(dbscan_predict(dbscan, np.array([test_vectors[3]]))[0]))

plt.figure(figsize=(10, 10))
colors = ['purple', 'red', 'blue']
plt.scatter(word_vectors[:, 0], word_vectors[:, 1], c=dbscan.labels_, cmap=matplotlib.colors.ListedColormap(colors), s=15)
plt.title('DBSCAN Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()
