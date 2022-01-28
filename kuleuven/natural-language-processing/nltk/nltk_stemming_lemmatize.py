import gensim
import pandas as pd
from gensim import corpora
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def lemmatize_stemming(text, stemmer):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def pre_process(text, stemmer=SnowballStemmer('english')):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token, stemmer))
    return result


doc_sample = "ratepayers group wants compulsory local govt voting"
words = [word for word in doc_sample.split(' ')]
print('\noriginal words:           ', words)
print('tokenized and lemmatized: ', pre_process(doc_sample))

stemmer = SnowballStemmer('english')
original_words = ['caresses', 'flies', 'or', 'but', 'dies', 'mules', 'denied', 'died', 'agreed', 'owned',
                  'humbled', 'sized', 'meeting', 'stating', 'siezing', 'itemization', 'sensational',
                  'traditional', 'reference', 'colonizer', 'plotted']
singles = [stemmer.stem(plural) for plural in original_words]
df = pd.DataFrame(data={'original word': original_words, 'stemmed': singles})
print("\nsecond example: ", df)
