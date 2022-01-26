from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess

def print_dictionary(dictionary):
    print("\nindexed words:")
    count = 0
    for k, v in dictionary.iteritems():
        print(k, v)
        count += 1


eachRowADocument = ["aba decides zend community noon",
                    "against decides",
                    "calls for infrastructure protection",
                    "air nz decides community",
                    "air community community community australian"]
documents = [[word for word in row.split(' ')] for row in eachRowADocument]
# documents = []
# for row in eachRowADocument:
#     words = [word for word in row.split(' ')]
#     documents.append(words)
# documents = pd.Series(documentsAsArray)
print("documents:\n", *documents, sep='\n')

dictionary = Dictionary(documents)
print_dictionary(dictionary)

# (token_id, token_count) 2-tuples
# print("bow_0: ", dictionary.doc2bow(documents[0]))
# print("bow_1: ", dictionary.doc2bow(documents[1]))
# print("bow_1: ", dictionary.doc2bow(documents[2]))
# print("bow_1: ", dictionary.doc2bow(documents[3]))
# print("bow_1: ", dictionary.doc2bow(documents[4]))
bow = [dictionary.doc2bow(doc) for doc in documents]
print('\nbow: ', *bow, sep='\n')


# Tokenize the docs
tokenized_list = [simple_preprocess(doc) for doc in eachRowADocument]
mydict = Dictionary()
mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list]
print('\nusing simple_preprocess: ', *mycorpus, sep='\n')