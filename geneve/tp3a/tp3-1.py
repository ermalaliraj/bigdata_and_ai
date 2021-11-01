# The method calculates the emission probability e(word|tag).
# The frequency of a "word" inside the file "gene.counts",  tagged as "tag".
#
# Example:
# Structure of "gene.counts", aggregates for scanned file "gene.train"
# 40 WORDTAG NOGENE Comparison
# 3367 WORDTAG NOGENE with
# 28 WORDTAG GENE alkaline
# ...
# ...
#
# Observations:
# The word Comparison appeared 40 time in the file tagged as NOGENE
# Total words tagged as NOGENE 25095  (40 of them are for the word Comparison)
# Total words tagged as GENE 8411
#
# Conclusion:
# The system calculates and returns: 40/25095.
#
# prob = compute_emission_parameter("Comparison", "NOGENE")
# print(prob) => 40/345128
def compute_emission_parameter(searchWord, searchTag):
    file_counts = open("./doc/gene.counts", "r")
    lines = file_counts.readlines()
    freq = 0
    sumCountsForSameTag = 0
    for line in lines:
        tokens = line.split()
        type = tokens[1]

        if type == "WORDTAG":
            count = int(tokens[0])
            tag = tokens[2]
            word = tokens[3]
            #
            if searchTag == tag:
                sumCountsForSameTag += 1

                if searchWord == word:
                    freq = count

    print(freq)
    # print(sumCountsForSameTag)
    # print(freq / sumCountsForSameTag)
    return freq / sumCountsForSameTag


# We need to predict emission probabilities for words in the test data that do not
# occur in the training data. One simple approach is to map infrequent words in
# the training data to a common class, and to treat unseen words as members of
# this class. Replace infrequent words (Count(x) < 5) in the training dataset with a
# common symbol _RARE_, then re-run countfreqs.py to produce counts that take
# the _RARE_ class into account.
def create_rare_emission_file(geneFile, geneCounts):
    file_counts = open(geneCounts, "r")
    wordCount = getDictionaryFromFile(file_counts); # {word, totOccerencesFound}
    infrequentWords = []

    for key in wordCount.keys():
        if wordCount[key] < 5:
            infrequentWords.append(key)

    file_gene = open(geneFile, "r")
    lines = file_gene.readlines()
    outputFile = geneFile + ".rare"
    file_rare = open(outputFile, "w+")
    for line in lines:
        row = line.split()

        if (len(row) == 0):
            newLine = line
        else:
            if (len(row) == 2):
                word = row[0]
                tag = row[1]
                if word in infrequentWords:
                    newLine = "_RARE_ " + tag + "\n"
                else:
                    newLine = line
            else:
                print("sdcsdfr")
                exit(1)

        file_rare.write(newLine)

    file_rare.write(newLine)
    file_counts.close()
    file_gene.close()
    file_counts.close()


# dictionary in format {word, totOccurrenciesFund}
# Search in the file all the rows of type WORDTAG and build the dictionary with the format {word, totOccurenciesFund}
def getDictionaryFromFile(f):
    wordCount = {}  # dictionary in format {word, totOccurenciesFund}
    lines = f.readlines()
    for line in lines:
        tokens = line.split()
        if tokens[1] == "WORDTAG":
            word = tokens[3]
            if word in wordCount:
                wordCount[word] += int(tokens[0])
            else:
                wordCount[word] = int(tokens[0])

    print(wordCount)
    return wordCount;


if __name__ == "__main__":
    freqWith = compute_emission_parameter("with", "NOGENE")
    freqcomparison = compute_emission_parameter("comparison", "GENE")
    print("Emission for the word 'with':", freqWith)
    print("Emission for the word 'comparison':", freqcomparison)
    print(freqcomparison)
    # create_rare_emission_file("gene.train", "gene.train.counts")
