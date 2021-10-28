# Create a script that takes as input a file of text data and displays the list of words contained in
# that file in alphabetical order, as well as the lines in which the words appear.

index_dict = {}  # catalog, map  {{word1, [lne1, line2, ...]}, {word2, [lne1, line2, ...]}
line_num = 0
file = open("austen.txt", "r")

for line in file:
    line_num += 1
    words = line.split()  # list
    for word in words:
        if word not in index_dict:
            index_dict[word] = []
        index_dict[word].append(line_num)

for word in sorted(index_dict):
    print("{", word, ", [", end="")
    for line in index_dict[word]:
        print(line, end=" ")
    print("] }")
