# Unigram Tagger ( TP3 - Question 1 > Third point)

def tagger(counts, dataset):
    f = open(counts, "r")
    wordCount = {}  # '_RARE_': {'GENE': '8732', 'NOGENE': '28781'}
    tagCount = {}  # GENE: 232323 , NOGENE: 545433
    for line in f.readlines():
        tokens = line.split()
        if len(tokens) == 4 and tokens[1] == "WORDTAG":
            word = tokens[3]
            tag = tokens[2]
            count = int(tokens[0])
            if word not in wordCount:
                wordCount[word] = {}
            wordCount[word][tag] = count
            if tag in tagCount:
                tagCount[tag] += count
            else:
                tagCount[tag] = count
    # print(len(wordCount))
    print(len(tagCount))
    f.close()
    f = open(dataset, "r")
    f1 = open(dataset + ".p1.out", "a+")

    for word in f.readlines():
        word = word.replace("\n", "") #remove the "new line" characters for simplifying ou
        if(word == ""):
            # if empty row, copy as it is in the new file
            f1.write(word + "\n")
        else:
            # tag the found word
            tagged_word = tag_word(word, wordCount, tagCount)
            f1.write(word + " " + tagged_word + "\n")

    f1.close()
    f.close()


# computes the tag for the given word by using arg max
def tag_word(word, wordCount, tagCount):
    if word not in wordCount:
        word = "_RARE_"
    max_emission_parameter = 0
    computed_tag = ''
    for tag in wordCount[word]:
        emission_parameter = wordCount[word][tag] / tagCount[tag]
        if emission_parameter > max_emission_parameter:
            max_emission_parameter = emission_parameter
            computed_tag = tag
    return computed_tag


if __name__ == '__main__':
    tagger("./doc/gene.key.counts", "./doc/gene.dev")
