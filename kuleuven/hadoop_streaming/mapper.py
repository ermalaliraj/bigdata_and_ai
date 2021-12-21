import sys

print("mapper..")
for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        print("{} {}".format(word, 1))

# file = open("text.txt")
# text = file.readlines()
#
# for line in text:
#     line = line.strip()
#     words = line.split()
#     for word in words:
#         print("{}\t{}".format(word, 1))
