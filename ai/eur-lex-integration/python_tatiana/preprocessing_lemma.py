import collections
import re
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import spacy

# nlp = en_core_web_sm.load(disable=['parser', 'ner'])
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

pd.set_option('max_colwidth', 150)

data_dir = "../output/oj/"
file_name = "reg_2016_679_akn.xml"


def to_string_utf8(document):
    return document.decode('utf-8')


def get_doc_data(filepath):
    tree = ET.parse(filepath)
    document = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
    document = to_string_utf8(document)
    document = re.sub('[ \t\n]+', ' ', document)
    return document


docContent = get_doc_data(data_dir + file_name)
print("docContent: ", docContent[0: 250], "...")
df = pd.DataFrame(data={'documentName': [], 'documentContent': []}, dtype=np.str_)
df.loc[1, 'documentName'] = 'filename1'
df.loc[1, 'documentContent'] = docContent

doc = nlp(docContent)

words_as_pos = []
for word in doc:
    if word.is_stop == False and len(word.text) > 2 and word.is_alpha:  # letters at least 3 characters
        words_as_pos.append(word.pos_)  # POS is more about the context of the features than frequencies of features

df['doc'] = df['documentContent'].apply(lambda x: nlp(x))
df['list_of_POSs'] = df['doc'].apply(lambda x: [word.pos_
                                                      for word in x if (word.is_stop==False) & \
                                                      (len(word.text)>2) & \
                                                      (word.is_alpha)
                                                      ])

# count total frequencies of words
POS_freq_counter = collections.Counter(words_as_pos)
s_POS_freq = pd.Series(POS_freq_counter, dtype=float)
s_POS_freq = s_POS_freq.sort_values(ascending=False)
df_tmp = pd.DataFrame(s_POS_freq, columns=['Frequency'], dtype=float)
# print("df_tmp:  \n", df_tmp)

df_tmp.plot.bar(alpha=0.5, color='c', legend=False, title='POS frequency in all texts combined')
plt.show()

selected_POSs = ['NOUN', 'VERB', 'ADJ', 'ADV']
print('selecting POSs:', selected_POSs)

# words_as_lemma = []
# for word in doc:
#     if word.is_stop == False and len(word.text) > 2 and word.is_alpha and word.pos_ in selected_POSs:
#         words_as_lemma.append(word.lemma_)
# final = " ".join(words_as_lemma)
# print("words_as_lemma: ", final[0: 150], "...")
# df_data = pd.DataFrame.from_records(words_as_lemma, columns=['words_as_lemma'])


df['list_of_lemmas'] = df['doc'].apply(lambda x: [word.lemma_
                                                            for word in x if (word.is_stop==False) & \
                                                            (len(word.text)>2) & \
                                                            (word.is_alpha) & \
                                                            (word.pos_ in selected_POSs)])

tmp_list = df['list_of_lemmas'].apply(set).apply(list).tolist()
list_of_lemmas = [lemma for sublist in tmp_list for lemma in sublist]

lemma_freq_counter = collections.Counter(list_of_lemmas)
s_lemma_freq = pd.Series(lemma_freq_counter)
print('Total number of unique lemmas: ', len(s_lemma_freq))

print("\nDistribution of lemmas' document counts: ", s_lemma_freq.describe(percentiles=[0.55, 0.65, 0.75, 0.85, 0.95, 0.97, 0.99]))

# look through to 20 most/least frequent lemmas
s_tmp = s_lemma_freq.sort_values(ascending=False)
df_tmp = pd.DataFrame({'Most freq words': list(s_tmp.index[:20]),
                       'M_freq': list(s_tmp.iloc[:20]),
                       'Least freq words': list(s_tmp.index[-20:]),
                       'L_freq': list(s_tmp.iloc[-20:])})

print ("df_tmp: \n", df_tmp)

# To reduce dimentionality of dictionary for topic modeling lemmas that have frequency count lower than 50th percentile and higer 99.9
#  percentile were deleted select upper and lower boundary for lemmas' count
up_pct = s_lemma_freq.quantile(0.99)
low_pct = s_lemma_freq.quantile(0.50)

print('Lemma count upper bound:', up_pct)
print('Lemma count lower bound:', low_pct)

# select lemmas
selected_lemmas = set(s_lemma_freq[(s_lemma_freq >= low_pct)&(s_lemma_freq <= up_pct)].index)
print('List of lemmas for topic modeling dictionary is reduced from', len(s_lemma_freq), 'to', len(selected_lemmas))
print("\nExample of selected lemmas:", list(selected_lemmas)[:5])

# select lemmas in each document if they belong to chosen list of lemmas
df['selected_list_of_lemmas'] = df['list_of_lemmas'].apply(lambda x: [l for l in x if l in selected_lemmas])