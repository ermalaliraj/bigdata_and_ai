# Tp3

-  Count frequencies


|gene.test|gene.test.counts|   |   |   |
|---|---|---|---|---|
| Third  |1 WORDTAG Third|   |   |   |
|,|511 WORDTAG ,|   |   |   |
|consistent |4 WORDTAG consistent|   |   |   |
|with |115 WORDTAG with|   |   |   |
|these |19 WORDTAG these|   |   |   |
|data |12 WORDTAG data|   |   |   |


|gene.key             |gene.key.counts             | gene.key.p1.out     |gene.key.rare     |
|---------------------|----------------------------|---------------------|------------------|
| BACKGROUND NOGENE   |5 WORDTAG NOGENE BACKGROUND | BACKGROUND NOGENE   |BACKGROUND NOGENE |
|: NOGENE             |61 WORDTAG NOGENE :         |: NOGENE             |: NOGENE          |
|Ischemic NOGENE      |1 WORDTAG NOGENE Ischemic   |Ischemic NOGENE      |_RARE_ NOGENE     |
|heart NOGENE         |5 WORDTAG NOGENE heart      |heart NOGENE         |heart NOGENE      |
|disease NOGENE       |8 WORDTAG NOGENE disease    |disease NOGENE       |disease NOGENE    |
|is NOGENE            |...                         |is NOGENE            |is NOGENE         |
|the NOGENE           |13193 1-GRAM NOGENE         |the NOGENE           |the NOGENE        |
|primary NOGENE       |1527 1-GRAM GENE            |primary NOGENE       |primary NOGENE    |


```
gene.key
BACKGROUND NOGENE
: NOGENE
Ischemic NOGENE
heart NOGENE
disease NOGENE
is NOGENE
the NOGENE
primary NOGENE


gene.key.counts
5 WORDTAG NOGENE BACKGROUND
61 WORDTAG NOGENE :
1 WORDTAG NOGENE Ischemic
5 WORDTAG NOGENE heart
8 WORDTAG NOGENE disease
...
13193 1-GRAM NOGENE
1527 1-GRAM GENE
483 2-GRAM * NOGENE


gene.key.p1.out
BACKGROUND NOGENE
: NOGENE
Ischemic NOGENE
heart NOGENE
disease NOGENE
is NOGENE


gene.key.rare
BACKGROUND NOGENE
: NOGENE
_RARE_ NOGENE
heart NOGENE
disease NOGENE
is NOGENE
the NOGENE
primary NOGENE
```


```
keyFile = "./doc/gene.key"
prediction_file = "./doc/dev/gene.dev.p1.out"
```
```
	precision 	recall 		F1-Score
GENE:	0.341112	0.774143	0.473559
```


```
keyFile = "./doc/gene.key"
prediction_file = "./doc/gene.key.p1.out"
```
```
	precision 	recall 		F1-Score
GENE:	0.341112	0.774143	0.473559
```


### See
[Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai)