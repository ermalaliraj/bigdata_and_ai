import sys


print("reducer..")

current_word = None
current_count = 0
word = None
# input comes from STDIN

file = open("mapper_output.txt")
lines = file.readlines()

# word_list = lines.split()  # convert the string to a list
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



# for line in text:
# # for line in sys.stdin:
#     line = line.strip()
#     if line == "":
#         quit()
#
#     word, count = line.split()
#
#     try:
#         count = int(count)
#     except ValueError:
#         continue
#
#     # works because Hadoop sorts map output
#     if current_word == word:
#         current_word += word
#     # else:
#         # if current_word:
#         #     print("{}\t{}".format(current_word, current_count))
#     current_count = count
#     current_word = word
#
#     print("{}\t{}".format(current_word, current_count))
#
# if current_word == word:
#     print("{}\t{}".format(current_word, current_count))
