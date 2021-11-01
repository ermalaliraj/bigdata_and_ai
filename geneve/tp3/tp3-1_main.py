from geneve.tp3.countfreqs import countNgrams


class Tagger:
    def __init__(self):
        ""


#     def sigmoid(self, x):
#         """
#         Takes in weighted sum of the inputs and normalizes them through between 0 and 1 through a sigmoid function
#         """
#         return 1 / (1 + np.exp(-x))
#
#
# def compute_emission_parameter(searchWord, searchTag, fileName):
#     file_counts = open(fileName, "r")
#     lines = file_counts.readlines()
#     wordFreq = 0
#     tagFreq = 0
#     for line in lines:
#         tokens = line.split()
#         type = tokens[1]
#
#         if type == "WORDTAG":
#             count = int(tokens[0])
#             tag = tokens[2]
#             word = tokens[3]
#             if searchTag == tag:
#                 tagFreq += count
#                 if searchWord == word:
#                     wordFreq = count
#
#     # print("Word '{0}' found {1} times, from a total of {2} {3}s, in the file {4}".format(searchWord, wordFreq, tagFreq, searchTag, file_counts.name))
#     return wordFreq / tagFreq
#
#
# # TP3- Question 1 (second point)
# # This function computes infrequent words in the gene.train corpus and replace them with _RARE_ tag.
# # Save the result in the new file gene_rare.train.
# # We need to predict emission probabilities for words in the test data that do not occur in the training data.
# # One simple approach is to map infrequent words in the training data to a common class,
# # and to treat unseen words as members of this class.
# # Replace infrequent words (Count(x) < 5) in the training dataset with a common symbol _RARE_,
# # then re-run countfreqs.py to produce counts that take the _RARE_ class into account.
# #
# # You can also replace infrequent words in the counts file. However, when doing so,
# # make sure to convert only words that have a frequency lower than 5 across both classes.
# def create_rare_emission_file(geneFile, geneCounts):
#     file_counts = open(geneCounts, "r")
#     wordCount = getDictionaryFromFile(file_counts);  # {word, totOccurrencesFound}
#     infrequentWords = []
#
#     for key in wordCount.keys():
#         if wordCount[key] < 5:
#             infrequentWords.append(key)
#
#     file_gene = open(geneFile, "r")
#     lines = file_gene.readlines()
#     outputFile = geneFile + ".rare"
#     file_rare = open(outputFile, "w+")
#     for line in lines:
#         row = line.split()
#
#         if len(row) == 0:
#             newLine = line
#         else:
#             if len(row) == 2:
#                 word = row[0]
#                 tag = row[1]
#                 if word in infrequentWords:
#                     newLine = "_RARE_ " + tag + "\n"
#                 else:
#                     newLine = line
#             else:
#                 print("gene file rows should be in the format 'word GENE|NOGENE'")
#                 exit(1)
#
#         file_rare.write(newLine)
#
#     file_rare.write(newLine)
#     file_counts.close()
#     file_gene.close()
#     file_counts.close()
#
#
# # dictionary in format {word, totOccurrencesFund}
# # Search in the file all the rows of type WORDTAG and build the dictionary with the format {word, totOccurrencesFund}
# def getDictionaryFromFile(f):
#     wordCount = {}  # dictionary in format {word, totOccurrencesFund}
#     lines = f.readlines()
#     for line in lines:
#         tokens = line.split()
#         if tokens[1] == "WORDTAG":
#             word = tokens[3]
#             if word in wordCount:
#                 wordCount[word] += int(tokens[0])
#             else:
#                 wordCount[word] = int(tokens[0])
#
#     # print(wordCount)
#     return wordCount;


if __name__ == "__main__":
    # countFreqs = CountFreqs()
    geneFileName = "./doc/gene.train"
    geneCountsFileName = "./doc/gene.train.counts"

    geneFile = open(geneFileName, "r")
    geneCountsFile = open(geneCountsFileName, "w")  # sys.stdout

    countNgrams(geneFile, 3, geneCountsFile)
    tagger = Tagger()
