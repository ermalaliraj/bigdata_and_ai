import pickle

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis


def deserializeFile(file_name):
    print("\nLoading ", file_name)
    with open(file_name, 'rb') as f:
        corpus = pickle.load(f)
    return corpus

lda_model = deserializeFile('./model/lda_eu_regulations_model.dat')
corpus = deserializeFile('./model/lda_eu_regulations_model_corpus.dat')
print("Loaded Regulations model and corpus data.")

print("Preparing visualisation... ")
visualisation = gensimvis.prepare(lda_model, corpus, lda_model.id2word, mds="mmds", R=30)
pyLDAvis.save_html(visualisation, 'LDA_Regulation_topics.html')
print("Created Visualization file: LDA_Regulation_topics.html")
