#compute emission probabilities matrix based on the count file
def compute_emission_probabs(count_file):
    f = open(count_file)
    tag_count = {}
    emissionProbs = {}
    for line in f:
        tokens = line.split()
        if len(tokens) > 1 and tokens[1] == '1-GRAM':
            tag_count[tokens[2]] = int(tokens[0])

    f = open(count_file)
    for line in f:
        tokens = line.split()
        if len(tokens) > 1 and tokens[1] == 'WORDTAG':
           emissionProbs[(tokens[3], tokens[2])] = float(tokens[0]) / tag_count[tokens[2]]

    f.close()
    return emissionProbs

#compute transition probabilities matrix based on the count file
def compute_transition_probs(count_file):
    f = open(count_file)
    bigram = {}
    transitionProb = {}
    for x in f.readlines():
        tokens = x.split()
        if len(tokens) > 1:
            if tokens[1] == '2-GRAM':
                bigram[(tokens[2], tokens[3])] = float(tokens[0])
            elif tokens[1] == '3-GRAM':
                transitionProb[(tokens[2], tokens[3], tokens[4])] = float(tokens[0])
    f.close()

    for x in transitionProb:
        __y, _y, y= x
        transitionProb[x] /= bigram[(__y, _y)]
    return transitionProb


def get_sentence(file):
    cur = []
    for x in file.readlines():
        if x == '\n':
            yield cur
            cur = []
            continue
        x = x.strip()
        cur.append(x)


def viterbi(sentence, emissionProbs, transitionProbs):
    p = {}
    bp = {}
    tags = set ()
    tags.add("GENE")
    tags.add("NOGENE")
    get_tags = lambda k: {'*'} if k == -1 or k == 0 else tags
    for k in range(0, len(sentence) + 1):
        p[k] = {}
        bp[k] = {}
        for u in get_tags(k - 1):
            p[k][u] = {}
            bp[k][u] = {}
            for v in get_tags(k):
                p[k][u][v] = 0
                bp[k][u][v] = ''
    p[0]['*']['*'] = 1

    for k in range(1, len(sentence) + 1):
        for u in get_tags(k - 1):
            for v in get_tags(k):
                val_max = None
                arg_max = None
                if (sentence[k - 1], v) in emissionProbs:
                    emit_val = emissionProbs[(sentence[k - 1], v)]
                else:
                    for x in tags:
                        if (sentence[k - 1], x) in emissionProbs:
                            emit_val = 0
                            break
                    else:
                        emit_val = emissionProbs[('_RARE_', v)]

                for w in get_tags(k - 2):
                    cur_max = p[k - 1][w][u] * transitionProbs[(w, u, v)] * emit_val
                    if val_max == None or cur_max > val_max:
                        val_max = cur_max
                        arg_max = w
                p[k][u][v] = val_max
                bp[k][u][v] = arg_max

    n = len(sentence)
    tags_compute = [''] * n
    val_max = None
    for u in get_tags(n - 1):
        for v in get_tags(n):
            cur_max = p[n][u][v] * transitionProbs[(u, v, 'STOP')]
            if val_max == None or cur_max > val_max:
                val_max = cur_max
                tags_compute[n - 2] = u
                tags_compute[n - 1] = v
    for k in range(n - 2, 0, -1):
        tags_compute[k - 1] = bp[k + 2][tags_compute[k]][tags_compute[k + 1]]
    #print (tags_compute)
    return tags_compute


def trigram_hmm_trigger(in_file, out_file, count_file):

    f_in = open(in_file)
    f_out = open(out_file, 'w')

    for sentence in get_sentence(f_in):
        tags = viterbi(sentence, compute_emission_probabs(count_file),  compute_transition_probs(count_file))
        for k in range(len(sentence)):
            cur_line = sentence[k].strip() + ' ' + tags[k] + '\n'
            f_out.write(cur_line)
        f_out.write('\n')

    f_in.close()
    f_out.close()


trigram_hmm_trigger('./doc/gene.test', './doc/gene.test.p2.out', './doc/gene_rare.counts')


