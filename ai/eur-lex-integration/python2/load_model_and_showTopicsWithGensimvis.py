import pickle

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

fileModelName = './model/lda_model_EU_REG_year-16-17-18-19-20-21.dat'
fileCampusName = './model/lda_model_EU_REG_year-16-17-18-19-20-21_campus.dat'
outputFile = 'LDA_EU_REG_year-16-17-18-19-20-21_topics.html'

def deserializeFile(file_name):
    print("\nLoading ", file_name)
    with open(file_name, 'rb') as f:
        corpus = pickle.load(f)
    return corpus

lda_model = deserializeFile(fileModelName)
corpus = deserializeFile(fileCampusName)
print("Loaded Regulations model and corpus data.")

print("Preparing visualisation... ")
visualisation = gensimvis.prepare(lda_model, corpus, lda_model.id2word, mds="mmds", R=30)
pyLDAvis.save_html(visualisation, outputFile)
print("Created Visualization file: ", outputFile)
