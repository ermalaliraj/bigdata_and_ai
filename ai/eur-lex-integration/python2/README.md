# LDA for OJ Regulations download form EUR-Lex


### 1. Build the model 
`load_data_and_create_LDA.py`

### 2. Run load_model_and_DBSCAN.py

<img src="./doc/dbscan.png" width="60%" height="auto">

```
Loading  ./model/lda_books_model.dat
Loading  ./model/lda_books_model_corpus.dat
Loaded Regulations model and corpus data.

First 5 topics:
(0, '0.035*"digital" + 0.032*"right" + 0.031*"term" + 0.026*"long" + 0.025*"capacity"')
(1, '0.000*"datum" + 0.000*"cabinet" + 0.000*"blast" + 0.000*"chill" + 0.000*"celsius"')
(2, '0.219*"datum" + 0.104*"personal" + 0.092*"processing" + 0.059*"subject" + 0.052*"authority"')
(3, '0.090*"dioxide" + 0.088*"titanium" + 0.075*"product" + 0.049*"cosmetic" + 0.032*"use"')

Total topics 100. Printing first 5:
['digital', 'right', 'term', 'long', 'capacity']
['datum', 'cabinet', 'blast', 'chill', 'celsius']
['datum', 'personal', 'processing', 'subject', 'authority']
['dioxide', 'titanium', 'product', 'cosmetic', 'use']
['accordance', 'animal', 'celsius', 'blast', 'chill']

Preparing visualisation...
Created Visualization file: LDA_Regulation_topics.html

Checking 100 topics loaded from the model
Total words in topics  500
Re-build corpus string concatenating all 1860 words sorted by words.index
Generated 229 tokens
word_vectors from tokens (229, 96)

Perform DBSCAN clustering from vector array or distance matrix. :-
DBSCAN labels with the word_vectors:
 [-1 -1 -1  0  0  0  0  0 -1 -1  0 -1  0  0  0  0  0 -1 -1  0  0  0  0  0
 -1  0  0  0  0  0  0  0  0 -1 -1 -1 -1  0  0  0  0 -1 -1 -1 -1 -1 -1  0
  0  0  0  0  0 -1 -1 -1 -1 -1  0  0  0  0 -1 -1 -1 -1 -1 -1 -1 -1 -1  0
 -1  0 -1 -1 -1  0 -1  0  0  0 -1 -1 -1  0  0  0  0  0  0  0  0  0  0 -1
  0 -1  0  0  0  0  0  0  0  0  0  0 -1 -1  0  0 -1 -1 -1 -1 -1  0 -1  0
  0  0 -1 -1 -1 -1 -1  0  0 -1  0  0  0 -1 -1 -1  0 -1 -1  0  0 -1 -1  0
  0  0  0  0 -1  0  0 -1 -1 -1  0  0 -1 -1 -1 -1  0 -1 -1 -1 -1  0  0  0
  0  0  0  0  0  0 -1 -1  0  0  0  0  0 -1 -1  0  0 -1 -1 -1 -1 -1 -1 -1
  0  0 -1  0  0 -1 -1 -1 -1  0 -1 -1  0  0 -1 -1 -1 -1 -1  0 -1 -1 -1  0
  0  0  0  0 -1  0  0 -1 -1 -1  0  0 -1]

test_tokens:  glandless international technology program
test_vectors from test_tokens[4x9] instead of 229x96
 [[-0.32610622 -0.41542953 -0.6061435  -0.540838    0.1473784 ]
 [-0.5150769   1.1283845   0.14961365 -0.5590282  -0.23367202]
 [-0.3714217   1.6924269   0.12218499 -0.85527736  0.96168256]
 [-0.50023943  0.5739464   0.75071084  0.38207614 -0.2480401 ]]

Some predictions
Label for glandless:-1
Label for international:-1
Label for technology:-1
Label for program:-1
```


 
### Links 
- [EUR-lex](https://eur-lex.europa.eu/content/welcome/about.html)


###
- [Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai) 