# Create a script that counts the frequency of each word in the text below

text = "Le poids politique de Lorient 'saffirme à partir de la Révolution française et la ville gagne un rôle administratif " \
       "à partir du premier Empire Les activités commerciales restent alors en retrait dans la première moitié du 19e siècle " \
       "en raison des conflits fréquents mais les activités militaires gagnent en importance"

text = text.lower()
word_list = text.split()  # convert the string to a list
word_count = {}  # dictionary for words and frequencies

for word in word_list:
    # if the key already exists, increment the value
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# display
for word in sorted(word_count):
    print(word, word_count[word])
