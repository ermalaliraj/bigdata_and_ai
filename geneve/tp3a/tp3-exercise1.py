#TP3- Question 1 (first point)
# This function computes emissiion probability e(word|tag)
def compute_emission_param(word, tag):
    f= open("./doc/gene.counts","r")
    lines = f.readlines()
    wordFreq=0
    tagFreq=0
    for line in lines:
        tokens = line.split()
        if tokens[1] == "WORDTAG":
            #print(line)
            if tokens[3] == word and tokens[2] == tag:
                wordFreq = int(tokens[0])
            if tokens[2] == tag:
                tagFreq+= int(tokens[0])
    return wordFreq/tagFreq

# TP3- Question 1 (second point)
# This function computes infrequent words in the gene.train corpus and replace them with _RARE_ tag
# produces the resulting corpus with file name : gene_rare.train
def compute_rare_emission_probab(word, tag):
    f = open("gene.counts", "r")
    wordCount = {}
    lines = f.readlines()
    for line in lines:
        tokens = line.split()
        if tokens[1] == "WORDTAG":
            lineWord = tokens[3]
            if lineWord in wordCount:
                wordCount[lineWord]+= int(tokens[0])
            else:
                wordCount[lineWord] = int(tokens[0])

    infrequentWords = []
    for k in wordCount.keys():
        if wordCount[k]< 5:
            infrequentWords.append(k)

    f2 = open("./doc/gene.train","r")
    lines = f2.readlines()
    f3 = open("./doc/gene_rare.train", "a+")
    for line in lines:
            newLine =" ".join(["_RARE_" if w in  infrequentWords else w for w in line.split()])
            print(newLine)
            f3.write(newLine+"\n")

    f.close()
    f2.close()
    f3.close()

if __name__== "__main__":
    freq =compute_emission_param("deoxymugineic", "NOGENE")
    print(freq)