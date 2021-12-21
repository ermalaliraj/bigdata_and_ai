print("reducer..")

file = open("mapper_output.txt")
lines = file.readlines()
word_count = {}  # dictionary for words and frequencies

for line in lines:
    line = line.strip()
    word, count = line.split()
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# display
for word in sorted(word_count):
    print(word, word_count[word])