# A concordancer is a tool for exploring textual data. Given a corpus of text data and a word, it extracts the occurrences
# of this word as well as the left and right contexts in which this word appears.
# For example, if given the preceding paragraph and the word "a", it would display the following result:
#                            a    concordancer is a to...
# a concordancer is          a    tool for exploring t...
# ... textual data. given    a    corpus of text data ...
# ...pus of text data and    a    word, it extracts th...

class Concordancier:
    def __init__(self, file_name):
        file = open(file_name)  # save the text as a list of lines
        self.text = file.readlines()

    def display(self, word, context_length=25):
        word = word.lower()
        count = 0;
        for line in self.text:
            line = line.strip().lower()
            match = line.find(word)
            while match >= 0:  # handle the first found, then loop in case there is more than one occurrence in the line
                count += 1;
                endMatch = match + len(word)

                # determine the beginning and the endMatch of context
                beginning_context = match - context_length
                end_context = endMatch + context_length

                context_left = "..." if (beginning_context > 0) else " "
                context_left = context_left + line[beginning_context:match]

                context_right = "..." if (end_context < len(line)) else " "
                context_right = line[endMatch:end_context] + context_right

                # format the contexts
                s = "{0:>{width}} {1} {2:<{width}}".format(context_left, word.upper(), context_right,
                                                           width=context_length + 5)
                print(s)
                match = line.find(word, endMatch)  # look for the next occurrence

        print("\nWord ", word, "found", count, "times")


c = Concordancier("austen.txt")
c.display("emma")
