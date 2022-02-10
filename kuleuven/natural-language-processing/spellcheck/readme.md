# Spell check

The process is implemented using `word2vec` embeddings. It is an adaptation of Peter Norvig's spell checker. 
It uses word2vec ordering of words to approximate word probabilities.

For this example pre-trained vectors trained on part of `Google News dataset` (about 100 billion words). 
The model contains 300-dimensional vectors for 3 million words and phrases.

The archive is available here: [GoogleNews-vectors-negative300.bin.gz](https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz)
(place it inside the folder `/data`)


###
- [Google word2vec](https://code.google.com/archive/p/word2vec/)
- [Back to Bid Data & AI](https://github.com/ermalaliraj/bigdata_and_ai)