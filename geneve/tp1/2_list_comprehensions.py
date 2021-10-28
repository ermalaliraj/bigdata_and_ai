# a) Let text1 be a sequence (list) of words. What does the following instruction do?
#     sum([len(w) for w in text1])
# Complete the instruction such that it computes the mean length of the words in text1.
# 
# b) Let the list ["she", "sells", "sea", "shells", "by", "the", "sea", "shore"] be given. Using list comprehensions, display:
#     1) all words that start with sh, and
#     2) all words that contain more than 4 characters.

text1 = "Le poids politique de Lorient 'saffirme à partir de la Révolution française et la ville gagne un rôle administratif " \
        "à partir du premier Empire Les activités commerciales restent alors en retrait dans la première moitié du 19e siècle " \
        "en raison des conflits fréquents mais les activités militaires gagnent en importance"

totalNonEmptyCharacters = sum([len(w) for w in text1])
totalCharacters = len(text1)

percentCharacters = totalNonEmptyCharacters / totalCharacters
totalEmptySpaces = totalCharacters - totalNonEmptyCharacters
print("totalCharacters: " + str(totalCharacters), "totalNonEmptyCharacters: " + str(totalNonEmptyCharacters))
print("percentCharacters: " + str(percentCharacters), "totalEmptySpaces: " + str(totalEmptySpaces))

word_list = text1.split()
count = 0
totalLength = 0
for word in word_list:
    totalLength = totalLength + len(word)
    count = count + 1

avgLength = totalLength / count
print("avgLength: " + str(avgLength))

list = ["she", "sells", "sea", "shells", "by", "the", "sea", "shore"]
for x in list:
    if x[:2] == 'sh':
        if len(x) > 4:
            print(x)
