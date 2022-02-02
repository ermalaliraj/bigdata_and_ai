import pickle

import matplotlib.pyplot as plt
import numpy as np
import spacy
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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


lda_model = deserializeFile('./model/lda_eu_regulations_model.dat')
corpus = deserializeFile('./model/lda_eu_regulations_model_corpus.dat')
print("Loaded Regulations model and corpus data.")

topics = show_topics(lda_model, 5)

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

print("\nPerform StandardScaler analysis")
ss = StandardScaler()
X = ss.fit_transform(word_vectors)
km = KMeans(n_clusters=20)
km.fit(X)
y_pred = km.predict(X)
print("y_pred:", y_pred)

plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='Paired')
plt.title("K-means")
plt.show()

test_words = ' '.join(['glandless', 'international', 'technology', 'program']).replace('-', ' ')
test_tokens = nlp(test_words)

test_vectors = []
for i in test_tokens:
    test_vectors.append(i.vector)
test_vectors = np.array(test_vectors)
test_pred = km.predict(test_vectors)
print("output labels : ", test_pred)
