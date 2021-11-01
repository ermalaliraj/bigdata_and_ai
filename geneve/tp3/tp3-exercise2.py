# TP3 - Question 2 - Point 1
# Function to compute transition parmaters
# _y denotes y-1
# __y denotes y-2

def compute_3gram_transition_parameters(y,_y,__y):
    f= open("./doc/gene.counts","r")
    ngram_counts = {}
    for x in f.readlines():
        if "WORDTAG" != x.split()[1]:
            tokens = x.split()
            if tokens[1] == "1-GRAM":
                ngram_counts[tokens[2]] = int(tokens[0])
            if tokens[1] == "2-GRAM":
                ngram_counts[tokens[2]+"-"+tokens[3]] = int(tokens[0])
            if tokens[1] == "3-GRAM":
                ngram_counts[tokens[2] + "-" + tokens[3] + "-" + tokens[4]] = int(tokens[0])
    print(ngram_counts)
    key = __y+"-"+_y+"-"+y
    if key not in ngram_counts:
        return 0
    else:
        return ngram_counts[key]/ngram_counts[__y+"-"+_y]

if __name__ == '__main__':
    print(compute_3gram_transition_parameters("STOP","GENE","GENE"))