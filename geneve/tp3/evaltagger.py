#! /usr/bin/env python3

# Initial version: Daniel Bauer <bauer@cs.columbia.edu>, Sep 29, 2011
# Current version: Yves Scherrer, UniGE, Nov 11 2014

import sys

"""
Evaluate gene tagger output by comparing it to a gold standard file.

Running the script on your tagger output like this
    - python evaltagger.py ./doc/gene.key ./doc/gene.dev.p1.out
will generate a table of results like this:

    Found 1457 GENEs. Expected 642 GENEs; Correct: 497.
		 precision      recall 		F1-Score
 GENE:   0.341112       0.774143    0.473559
"""


def corpus_iterator(corpus_file, with_logprob=False):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    tagfield = with_logprob and -2 or -1

    try:
        while l:
            line = l.strip()
            if line:  # Nonempty line
                # Extract information from line.
                # Each line has the format
                # word ne_tag [log_prob]
                fields = line.split(" ")
                ne_tag = fields[tagfield]
                word = " ".join(fields[:tagfield])
                yield word, ne_tag
            else:  # Empty line
                yield (None, None)
            l = corpus_file.readline()
    except IndexError:
        sys.stderr.write("Could not read line: \n\n")
        sys.stderr.write(line)
        if with_logprob:
            sys.stderr.write("Did you forget to output log probabilities in the prediction file?\n")
        sys.exit(1)


class NeTypeCounts(object):
    """
    Stores true/false positive/negative counts for each NE type.
    """

    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

    def get_precision(self):
        return self.tp / (self.tp + self.fp)

    def get_recall(self):
        return self.tp / (self.tp + self.fn)

    def get_accuracy(self):
        return (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)


class Evaluator(object):
    """
    Stores global true/false positive/negative counts.
    """

    ne_classes = ["GENE"]

    def __init__(self):
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

        # Initialize an object that counts true/false positives/negatives
        # for each NE class
        self.class_counts = {}
        for c in self.ne_classes:
            self.class_counts[c] = NeTypeCounts()

    def compare(self, gold_standard, prediction):
        """
        Compare the prediction against a gold standard. Both objects must be
        generator or iterator objects that return a (word, ne_tag) tuple at a
        time.
        """

        # Define a couple of tags indicating the status of each stream
        curr_pred_type = None  # prediction stream was previously in a named entity
        curr_pred_start = None  # a new prediction starts at the current token
        curr_gs_type = None  # prediction stream was previously in a named entity
        curr_gs_start = None  # a new prediction starts at the current token

        total = 0
        for gs_word, gs_type in gold_standard:  # Move through the gold standard stream
            pred_word, pred_type = next(prediction)  # Get the corresponding item from the prediction stream

            # Make sure words in both files match up
            if gs_word != pred_word:
                sys.stderr.write("Could not align gold standard and predictions in line {}.\n".format(total + 1))
                sys.stderr.write("Gold standard: {}  Prediction file: {}\n".format(gs_word, pred_word))
                sys.exit(1)

                # Check if a named entity ends here in either stream.
            # This is the case if we are currently in an entity and either
            #   - end of sentence
            #   - current word is marked O
            #   - new entity starts (B - or I with different NE type)
            pred_ends = curr_pred_type != None and ((pred_type == None or pred_type == "NOGENE") or (
                        curr_pred_type != pred_type and pred_type == "GENE"))
            gs_ends = curr_gs_type != None and (
                        (gs_type == None or gs_type == "NOGENE") or (curr_gs_type != gs_type and gs_type == "GENE"))

            # Check if a named entity starts here in either stream.
            # This is tha case if this is not the end of a sentence and
            #   - This is not the end of a sentence
            #   - New entity starts (B, I after O or at begining of sentence or
            #       I with different NE type)
            if pred_word != None:
                pred_start = (curr_pred_type == None and pred_type == "GENE") or (
                            curr_pred_type != None and curr_pred_type != pred_type and pred_type == "GENE")
                gs_starts = (curr_gs_type == None and gs_type == "GENE") or (
                            curr_gs_type != None and curr_gs_type != gs_type and gs_type == "GENE")

            else:
                pred_start = False
                gs_starts = False

                # For debugging:
            # print pred_word, gs_tag, pred_tag, pred_ends, gs_ends, pred_start, gs_starts

            # Now try to match up named entities that end here

            if gs_ends and pred_ends:  # GS and prediction contain a named entity that ends in the same place

                # If both named entities start at the same place and are of the same type
                if curr_gs_start == curr_pred_start and curr_gs_type == curr_pred_type:
                    # Count true positives
                    self.tp += 1
                    self.class_counts[curr_pred_type].tp += 1
                else:  # span matches, but label doesn't match: count both a true positive and a false negative
                    self.fp += 1
                    self.fn += 1
                    self.class_counts[curr_pred_type].fp += 1
                    self.class_counts[curr_gs_type].fn += 1
            elif gs_ends:  # Didn't find the named entity in the gold standard, count false negative
                self.fn += 1
                self.class_counts[curr_gs_type].fn += 1
            elif pred_ends:  # Named entity in the prediction doesn't match one int he gold_standard, count false positive
                self.fp += 1
                self.class_counts[curr_pred_type].fp += 1
            elif curr_pred_type == None and curr_pred_type == None:  # matching O tag or end of sentence, count true negative
                self.tn += 1
                for c in self.ne_classes:
                    self.class_counts[c].tn += 1

            # Remember that we are no longer in a named entity
            if gs_ends:
                curr_gs_type = None
            if pred_ends:
                curr_pred_type = None

            # If a named entity starts here, remember it's type and this position
            if gs_starts:
                curr_gs_start = total
                curr_gs_type = gs_type
            if pred_start:
                curr_pred_start = total
                curr_pred_type = pred_type
            total += 1

    def print_scores(self):
        """
        Output a table with accuracy, precision, recall and F1 score.
        """

        print("Found {} GENEs. Expected {} GENEs; Correct: {}.\n".format(self.tp + self.fp, self.tp + self.fn, self.tp))

        if self.tp + self.tn + self.fp + self.fn == 0:  # There was nothing to do.
            acc = 1
        else:
            acc = (self.tp + self.tn) / float(self.tp + self.tn + self.fp + self.fn)

        if self.tp + self.fp == 0:  # Prediction didn't annotate any NEs
            prec = 1

        else:
            prec = self.tp / float(self.tp + self.fp)

        if self.tp + self.fn == 0:  # Prediction marked everything as a NE of the wrong type.
            rec = 1
        else:
            rec = self.tp / float(self.tp + self.fn)

        print("\tprecision \trecall \t\tF1-Score")
        fscore = (2 * prec * rec) / (prec + rec)
        # print "Total:\t %f\t%f\t%f" % (prec, rec, fscore)
        for c in self.ne_classes:
            c_tp = self.class_counts[c].tp
            c_tn = self.class_counts[c].tn
            c_fp = self.class_counts[c].fp
            c_fn = self.class_counts[c].fn
            if (c_tp + c_tn + c_fp + c_fn) == 0:
                c_acc = 1
            else:
                c_acc = (c_tp + c_tn) / float(c_tp + c_tn + c_fp + c_fn)

            if (c_tp + c_fn) == 0:
                sys.stderr.write("Warning: no instances for entity type {} in gold standard.\n".format(c))
                c_rec = 1
            else:
                c_rec = c_tp / float(c_tp + c_fn)
            if (c_tp + c_fp) == 0:
                sys.stderr.write(
                    "Warning: prediction file does not contain any instances of entity type {}.\n".format(c))
                c_prec = 1
            else:
                c_prec = c_tp / float(c_tp + c_fp)

            if c_prec + c_rec == 0:
                fscore = 0
            else:
                fscore = (2 * c_prec * c_rec) / (c_prec + c_rec)
            print("{}:\t{:.6f}\t{:.6f}\t{:.6f}".format(c, c_prec, c_rec, fscore))


def usage():
    sys.stderr.write("""
    Usage: python eval_gene_tagger.py [key_file] [prediction_file]
        Evaluate the gene-tagger output in prediction_file against
        the gold standard in key_file. Output accuracy, precision,
        recall and F1-Score.\n""")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    gs_iterator = corpus_iterator(open(sys.argv[1]))
    pred_iterator = corpus_iterator(open(sys.argv[2]), with_logprob=False)
    evaluator = Evaluator()
    evaluator.compare(gs_iterator, pred_iterator)
    evaluator.print_scores()
