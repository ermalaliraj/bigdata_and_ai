# TP3- Question 1 (first point)
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
def compute_emission_parameter(searchWord, searchTag, fileName):
    file_counts = open(fileName, "r")
    lines = file_counts.readlines()
    wordFreq = 0
    tagFreq = 0
    for line in lines:
        tokens = line.split()
        type = tokens[1]

        if type == "WORDTAG":
            count = int(tokens[0])
            tag = tokens[2]
            word = tokens[3]
            if searchTag == tag:
                tagFreq += count
                if searchWord == word:
                    wordFreq = count

    # print("Word '{0}' found {1} times, from a total of {2} {3}s, in the file {4}".format(searchWord, wordFreq, tagFreq, searchTag, file_counts.name))
    return wordFreq / tagFreq


def compute_emission_parameter_absolute(searchWord, fileName):
    file_counts = open(fileName, "r")
    lines = file_counts.readlines()
    wordFreq = 0
    totalCount = 0
    for line in lines:
        tokens = line.split()
        type = tokens[1]

        if type == "WORDTAG":
            count = int(tokens[0])
            totalCount += count
            word = tokens[2]
            if searchWord == word:
                wordFreq += count

    return wordFreq / totalCount


# TP3- Question 1 (second point)
# This function computes infrequent words in the gene.train corpus and replace them with _RARE_ tag.
# Save the result in the new file gene_rare.train.
# We need to predict emission probabilities for words in the test data that do not occur in the training data.
# One simple approach is to map infrequent words in the training data to a common class,
# and to treat unseen words as members of this class.
# Replace infrequent words (Count(x) < 5) in the training dataset with a common symbol _RARE_,
# then re-run countfreqs.py to produce counts that take the _RARE_ class into account.
#
# You can also replace infrequent words in the counts file. However, when doing so,
# make sure to convert only words that have a frequency lower than 5 across both classes.
def create_rare_emission_file(geneCounts, geneFile):
    print("Replacing non frequent words with '_RARE_'")
    file_counts = open(geneCounts, "r")
    wordCount = getDictionaryFromFile(file_counts)  # {word, totOccurrencesFound}
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

        if len(row) == 0:
            newLine = line
        else:
            if len(row) == 2:
                word = row[0]
                tag = row[1]
                if word in infrequentWords:
                    newLine = "_RARE_ " + tag + "\n"
                else:
                    newLine = line
            else:
                print("gene file rows should be in the format 'word GENE|NOGENE'")
                exit(1)

        file_rare.write(newLine)

    print("Wrote {0} lines in the file {1}".format(len(lines), file_rare.name))
    file_rare.write(newLine)
    file_counts.close()
    file_gene.close()
    file_counts.close()


# dictionary in format {word, totOccurrencesFund}
# Search in the file all the rows of type WORDTAG and build the dictionary with the format {word, totOccurrencesFund}
def getDictionaryFromFile(f):
    wordCount = {}  # dictionary in format {word, totOccurrencesFund}
    lines = f.readlines()
    for line in lines:
        tokens = line.split()
        if tokens[1] == "WORDTAG":
            word = tokens[3]
            if word in wordCount:
                wordCount[word] += int(tokens[0])
            else:
                wordCount[word] = int(tokens[0])

    # print(wordCount)
    return wordCount


if __name__ == "__main__":
    geneCounts = "./doc/gene.train.counts"

    comparisonNogene = compute_emission_parameter("comparison", "NOGENE", geneCounts)
    print("Emission for the word 'comparison' NOGENE:", comparisonNogene)
    comparisonGene = compute_emission_parameter("comparison", "GENE", geneCounts)
    print("Emission for the word 'comparison': GENE", comparisonGene)

    ofNOGene = compute_emission_parameter("of", "NOGENE", geneCounts)
    print("\nEmission for the word 'with' NOGENE:", ofNOGene)
    ofGene = compute_emission_parameter("of", "GENE", geneCounts)
    print("Emission for the word 'with' GENE:", ofGene)

    # create_rare_emission_file("gene.train", "gene.train.counts")
    create_rare_emission_file("./doc/gene.train", "./doc/gene.train.counts")
