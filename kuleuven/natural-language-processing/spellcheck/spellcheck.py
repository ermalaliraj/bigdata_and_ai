import pickle
import re

import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('./data/GoogleNews-vectors-negative300.bin.gz', binary=True)
words = model.index_to_key
print("words[:100]: ", words[:100])

dict_tmp = dict(enumerate(words))
word_rank = dict(zip(dict_tmp.values(), dict_tmp.keys()))
print("dict(list(word_rank.items())[:5]) ", dict(list(word_rank.items())[:5]))

""" Following steps are simple modification of Peter Norvig's code. 
Instead of computing the frequency of each word we use the word ranks stored in word_rank dictionary."""


def words(text):
    return re.findall(r'\w+', text.lower())


def P(word):
    """ Probability of `word`.
    Use inverse of rank as proxy
    returns 0 if the word isn't in the dictionary
    """
    return - word_rank.get(word, 0)


def correction(word):
    """ Most probable spelling correction for word. """
    return max(candidates(word), key=P)


def candidates(word):
    """ Generate possible spelling corrections for word. """
    word = re.sub('[^a-zA-Z0-9]', '0', word)
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words):
    """ The subset of `words` that appear in the dictionary word_rank. """
    return set(w for w in words if w in word_rank)


def edits1(word):
    """ All edits that are one edit away from `word`. """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """ All edits that are two edits away from `word`. """
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# spell check examples
print('"Cle3n" is transformed to "', correction('Cle3n'), '"')
print('"qalty" is transformed to "', correction('quality'), '"')

print('\nNOTE: missing spaces are not corrected and might generate errors of spell correction:')
print('"thetable" is transformed to "', correction('thetable'), '"')

print('\nNOTE: empty strings generate a single letter word surraunded by spaces:')
print('"" is transformed to "', correction(''), '"')
print('IT WILL BE USED TO MARKE END OF A SENTENCE')

# Erroneous words that might appear in the text after spell checking will be deleted during text pre-processing.
# Since most likely they will have low count of appearances in the text (it is unlikely that > 500 people will make the same mistake over and over).
# Low count words will be deleted to reduce dimensionality of the dictionary of words that is used in the topic modeling.


input_folder = './data/'
output_folder = './data/'
file_name = 'text.txt'

with open(input_folder + file_name, 'rb') as f:
    df_data = pickle.load(f)

print("df_data.tail(1).T ", df_data.tail(1).T)

# split text on words
df_data['words'] = df_data['text'].str \
    .replace(',', ' ').str \
    .replace('[\t\n\r\f\v]', '. ').str \
    .replace(' +', ' ').str \
    .split('\W')

print(df_data['text'].iloc[0])
print('\nTransformed to:\n')
print(df_data['words'].iloc[0])

# # since spell checking goes through each word in each text, full data check will take a lot of time without a parallel processing
# def parallelize_dataframe(df, func, n_cores=4):
#     """
#     The function breaks the data frame (df) into n_cores parts,
#     and spawns n_cores processes which apply the function to all the pieces.
#
#     Once the function (func) is applied to all the split data frames,
#     the split data frames are concatenated in the resulting data frame
#     which is returned as an output.
#
#     input:
#          df - as pandas data frame
#          func - function to be applied on the df
#          n_cores - as integer, number of splits for data frame
#     output
#          df after application of the specified function
#     """
#     df_split = np.array_split(df, n_cores)
#     pool = Pool(n_cores)
#     df = pd.concat(pool.map(func, df_split))
#     pool.close()
#     pool.join()
#     return df
#
#
# def spell_check(df):
#     """
#     spell check each word in the column "words" that represents list of tokens from the text
#     and concatenate corrected words in a single text for each doc
#     """
#     df['spell_checked_text'] = df['words'] \
#         .apply(lambda x: ' '.join([correction(word) if len(word) != 1 else word for word in x]))
#     return df
#
#
# # CHECK HOW MANY n_cores YOU CAN USE
# # OPERATIONAL MEMORY CONSTRAIN: you need at least 20G of free RAM to run this step using all data (or do in chunks)
# # run spell check in parallel to speed-up calculations (less than 15 minutes on my machine with parallelization)
# df_data = parallelize_dataframe(df_data, spell_check, n_cores=15)
