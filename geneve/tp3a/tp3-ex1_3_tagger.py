# Unigram Tagger ( TP3 - Question 1 > Third point)

# Implement a simple gene tagger that always produces the tag y∗ = argmaxy e(x | y) for each word x.
# Make sure the tagger uses the _RARE_ word probabilities for rare and unseen words.
# The tagger should take the counts file (gene.key.counts) and the development dataset (gene.dev) as input,
# and produce as output predictions (gene.dev.p1.out) in the same format as the training dataset.

def tagger(fileGene, fileCounts):
    file_counts = open(fileCounts, "r")
    wordCount = {}  # {'BACKGROUND': {'NOGENE': '5'}, {'GENE': '0'}}, ...}
    tagCount = {}  # map the totals for each tag {GENE: 749 , NOGENE: 3732}
    for line in file_counts.readlines():
        tokens = line.split()
        if tokens[1] == "WORDTAG":
            tag = tokens[2]
            count = int(tokens[0])
            word = tokens[3]
            if word not in wordCount:
                wordCount[word] = {}  #

            wordCount[word][tag] = count

            if tag not in tagCount:
                tagCount[tag] = count  # add the tag first time we find it
            else:
                tagCount[tag] += 1  # add the count of genes found to the totals for that tag

    print("total WORDTAG's in file", fileGene, len(wordCount))
    print("total NOGENE", tagCount['NOGENE'], "total GENE", tagCount['GENE'])
    file_counts.close()

    file_gene = open(fileGene, "r")
    file_output = open(fileGene + ".p1.out", "w+")

    for word in file_gene.readlines():
        word = word.replace("\n", "")  # remove the "new line" characters
        if (word == ""):
            # if empty row, copy as it is in the new file
            file_output.write(word + "\n")
        else:
            # tag the found word
            tagged_word = tag_word(word, wordCount, tagCount)
            file_output.write(word + " " + tagged_word + "\n")

    file_output.close()
    file_gene.close()


# calculates the emission for a specific word for both GNE and NOGENE tag and return the highest
def tag_word(word, wordCount, tagCount):
    if word not in wordCount:
        word = "_RARE_"

    maxCalculatedEmission = 0
    calculatedTag = ''

    for tag in wordCount[word]:
        emission = wordCount[word][tag] / tagCount[tag]
        if emission > maxCalculatedEmission:
            maxCalculatedEmission = emission
            calculatedTag = tag
    return calculatedTag


if __name__ == '__main__':
    tagger("./doc/gene.dev", "./doc/gene.key.counts")
