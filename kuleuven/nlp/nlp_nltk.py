import os
import re

import nltk.corpus
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import word_tokenize
from nltk.util import bigrams, trigrams, ngrams

# print(os.listdir(nltk.data.find("corpora")))
print("brown.words: ", brown.words())
print("nltk.corpus.gutenberg.fileids(): ", nltk.corpus.gutenberg.fileids())
print("shakespeare-hamlet.txt: ", nltk.corpus.gutenberg.words('shakespeare-hamlet.txt'))

hamlet = nltk.corpus.gutenberg.words('shakespeare-hamlet.txt')

for word in hamlet[:500]:
    print(word, sep=' ', end=' ')

print("\n")
AI = "According to the father of Artificial Intelligence, John McCarthy, it is “The science and engineering of making " + os.sep + \
     "intelligent machines, especially intelligent computer programs”."  "Artificial Intelligence is a way of making a computer, " + os.sep + \
     "a computer-controlled robot, or a software think intelligently, in the similar manner the intelligent humans think. " + os.sep + \
     "AI is accomplished by studying how human brain thinks, and how humans learn, decide, and work while trying to solve a problem, " + os.sep + \
     "and then using the outcomes of this study as a basis of developing intelligent software and systems."

AI_tokens = word_tokenize(AI)
print("AI_tokens: ", len(AI_tokens), AI_tokens)

fdist = FreqDist()

for word in AI_tokens:
    fdist[word.lower()] += 1
print("artificial count: ", fdist['artificial'])
print("fdist.most_common: ", fdist.most_common())

AI_blank = blankline_tokenize(AI)
print("AI_blank: ", len(AI_blank), AI_blank)
print("first paragraph: ", AI_blank[0])

#
string = "The best and most beautiful things in the world cannot be seen or even touched, they must be felt with the heart"
quotes_tokens = nltk.word_tokenize(string)
print("\nquotes_tokens: ", quotes_tokens)

quotes_bigrams = list(bigrams(quotes_tokens))
print("quotes_bigrams: ", quotes_bigrams)
quotes_trigrams = list(trigrams(quotes_tokens))
print("quotes_trigrams: ", quotes_trigrams)
quotes_5trigrams = list(ngrams(quotes_tokens, 5))
print("quotes_5trigrams: ", quotes_5trigrams)

pst = nltk.PorterStemmer()
words_to_stem = ["give", "giving", "given", "gave"]
for word in words_to_stem:
    print(word + ":", pst.stem(word))

print("\n")
lst = nltk.LancasterStemmer()
for word in words_to_stem:
    print(word + ":", lst.stem(word))

# print("\n")
# word_lem = nltk.WordNetLemmatizer()
# print("corpora: " + word_lem.lemmatize("corpora"))
# for word in words_to_stem:
#     print(word + ":", word_lem.lemmatize(word))

print("stopwords.words('english'): " + str(stopwords.words('english')))
punctuation = re.compile(r'[-.?!,:;()|0-9]')
post_punctuation = []

print("\n")
for word in AI_tokens:
    word = punctuation.sub("", word)
    if len(word) > 0:
        post_punctuation.append(word)
print("post_punctuation: ", post_punctuation)

print("\n")
sent = "Timothy is a natural when it comes to drawing"
sent_tokens = word_tokenize(sent)
for token in sent_tokens:
    print(nltk.pos_tag([token]))

print("\n")
NE_sent = "the US President stays in the WHITE HOUSE"
NE_tokens = word_tokenize(NE_sent)
NE_tags = nltk.pos_tag(NE_tokens)
NE_chunk = nltk.ne_chunk(NE_tags)
print("NE_tokens: ", NE_tokens)
print("NE_tags: ", NE_tags)
print("NE_chunk: \n", NE_chunk)

print("\n")
new = "the big cat ate the little mouse who was after fresh cheese"
new_tokens = nltk.pos_tag(word_tokenize(new))
print("new_tokens: ", new_tokens)

grammar_np = r"NP: {<DT>?<JJ>*<NN>}"
chunk_parser = nltk.RegexpParser(grammar_np)
chunk_result = chunk_parser.parse(new_tokens)
print("chunk_result: ", chunk_result)


