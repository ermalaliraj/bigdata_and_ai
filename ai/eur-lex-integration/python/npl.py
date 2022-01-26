import xml.etree.ElementTree as ET

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

tree = ET.parse('../output/oj/reg_2016_679_akn.xml')


def to_string_utf8(document):
    return document.decode('utf-8')


documents = ET.tostringlist(tree.getroot(), encoding='utf-8', method='text')
documents = list(map(to_string_utf8, documents))  # utf-8
# documents = ' '.join(documents).split() # 1 word per line
print("Total document", len(documents))
# print(*documents, sep="\n")

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)
# print(X)

true_k = 5
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

# how much an LDA topic layer would help to create relevant and understandable cluster?
# 1) LDA topic layer => set of topics   (10 topics)
#         can the number of topics been utocorrected
# 2) Use topics for further analysis

# topoi modleing layer, instead of using terms
# lda to build topic layer and run the model of clustering over those topics

# size of the cluster
# number of the documents used


print("\n")
print("Prediction")


# 1. create list of topics
#

# Cluster 4:
# data
# controller
# processing
# processor
# shall
# personal
# article
# referred
# protection
# risk



# Cluster 4:
# Privacy  (60%)
# Energy  (30%)
# Internet   (68%)
# AI (98%)
