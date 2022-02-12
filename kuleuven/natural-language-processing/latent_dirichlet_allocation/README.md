# Latent Dirichlet Allocation 

Divide documents by topic they talk too. 

### Latent Dirichlet Allocation 
`Latent Dirichlet Allocation`  is a machine that produces documents.

### Dirichlet Distributions
`Dirichlet Distributions` we have parameter ` alpha` 
- 1, uniform on the left.
- < 1, uniform to the corners.
- > 1, uniform at the center.
 
 
### Two Dirichlet Distributions

<img src="./doc/documents-topics.JPG" width="30%" height="auto"> <img src="./doc/topics-words.JPG" width="30%" height="auto"> 

The one on the left associates documents with their corresponding topics. 
The on on the right associates topics with their corresponding words.

### How to put these together?

<img src="./doc/lda_machine.JPG" width="20%" height="auto"> 
We put those together rememebring that LDA is a machien that produces documents.
This machine has some settings that we adjust. 
These settings are exactly the `Two Dirichlet Distributions` above.
The way we adjust the settings is by moving the points inside the distributions.
We produce a document for each setting.
 

### Probability that a particular document comes out of a machine

<img src="./doc/lda_generation.JPG" width="99%" height="auto">
The generated article is just a combiantion of words: Planet, galaxy, ball, plannet, galaxy, referendum, galaxy, ball and referendum.

Using these mode, we generate a collection fo documents and we go back and check if they look like the once we have from the beginning. 
Notice that to every yellow dot in the left distribution a document corresponds. They are according to the topics given by the yellow dots and their position.
<br/>

The probability we get the same article is very low, but we choose the closest to the same.

<img src="./doc/lda_generation_check2.JPG" width="80%" height="auto">

### 
<img src="./doc/lda_generation_map.JPG" width="80%" height="auto">
<img src="./doc/lda.JPG" width="80%" height="auto">



```  
pip install --user pyldavis
pip install --user spacy
python -m spacy download en   # now you can spacy.load('en_core_web_sm')
```

### Links 
- [Video Tutorial](https://www.youtube.com/watch?v=T05t-SqKArY&t=822s)
- [LDA news headlines by Susan Li](https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24)
- [LDA news headlines github](https://github.com/susanli2016/NLP-with-Python/blob/master/LDA_news_headlines.ipynb)
- [Introduction to LDA](http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/)
https://www.youtube.com/watch?v=1_jq_gWFUuQ


###
- [Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai) 