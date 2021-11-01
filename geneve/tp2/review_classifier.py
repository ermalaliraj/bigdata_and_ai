#! /usr/bin/python3
# -*- coding: utf-8 -*-

import math
import os
import re

# Global varialbles 

# Two classes: positive and negative
classes = ("pos", "neg")

# Words with frequencies, no group distinguish
word_frequencies = {}

# Words with frequencies, with group distinguish
word_frequencies_per_class = {}

# Word number per group
total_words_per_class = {}

# Confusion matrix
confusion_matrix = {}


# Tokenization
def tokenize_message(l):
    # Regular expression from http://www.nltk.org/_modules/nltk/tokenize/regexp.html
    tokens = re.findall(r'\w+|[^\w\s]+', l)
    return tokens


# reads all documents, transforms them into a list of words and take vocabularies for training
def training(tokenize=False, lowercase=False):
    for c in classes:
        word_frequencies_per_class[c] = {}
        total_words_per_class[c] = 0
        nb_msg = 0

        for msg in os.listdir("data/train/" + c):
            nb_msg += 1
            f = open("data/train/" + c + "/" + msg, encoding="utf-8")
            if tokenize:
                tokens = tokenize_message(f.read())
            else:
                tokens = f.read().split()

            for token in tokens:
                if lowercase:
                    token = token.lower()
                word_frequencies.setdefault(token, 0)
                word_frequencies[token] += 1
                # increment the frequency of the word in the vocabulary of the current group
                word_frequencies_per_class.setdefault(c, {})
                word_frequencies_per_class[c].setdefault(token, 0)
                word_frequencies_per_class[c][token] += 1
                total_words_per_class[c] += 1
            f.close()
        print("Training finished for {0} ({1} files, {2} words)".format(c, nb_msg, total_words_per_class[c]))


# ---------------------------------------

def testing(tokenize=False, lowercase=False, count_features=False, smoothing=False):
    for true_class in classes:
        confusion_matrix[true_class] = {}
        vocabulary_size = len(word_frequencies)
        for msg in os.listdir("data/test/" + true_class):
            f = open("data/test/" + true_class + "/" + msg, encoding="utf-8")
            if tokenize:
                tokens = tokenize_message(f.read())
            else:
                tokens = f.read().split()
            if lowercase:
                tokens = [token.lower() for token in tokens]
            if count_features == False:
                tokens = set(tokens)

            results = {}
            for predicted_class in classes:
                # Determine the prior probability of the group
                predicted_prob = math.log(0.5)

                # For each separate word that appears in the test file, we add the log probability to the given group
                for t in tokens:
                    # No need to test the stopwords
                    if smoothing:
                        if t in word_frequencies:
                            predicted_prob += math.log((word_frequencies_per_class[predicted_class].get(t, 0) + 1) / (
                                    total_words_per_class[predicted_class] + vocabulary_size))
                    else:
                        # If t appears in word_frequencies_per_class[pos] as well as in word_frequencies_per_class[neg]
                        if all([t in word_frequencies_per_class[pc] for pc in classes]):
                            predicted_prob += math.log(
                                word_frequencies_per_class[predicted_class][t] / total_words_per_class[predicted_class])
                results[predicted_class] = predicted_prob

            max_class = max(results, key=lambda x: results[x])

            # add the result to the confusion matrix for the evaluation
            confusion_matrix[true_class].setdefault(max_class, 0)
            confusion_matrix[true_class][max_class] += 1
            f.close()


def evaluation():
    tp = confusion_matrix["pos"].get("pos", 0)  # True positives
    tn = confusion_matrix["neg"].get("neg", 0)  # True negatives
    fp = confusion_matrix["neg"].get("pos", 0)  # False positives
    fn = confusion_matrix["pos"].get("neg", 0)  # False negatives

    precision_pos = tp / (tp + fp)
    precision_neg = tn / (tn + fn)
    recall_pos = tp / (tp + fn)
    recall_neg = tn / (tn + fp)
    f1_pos = (2 * recall_pos * precision_pos) / (recall_pos + precision_pos)
    f1_neg = (2 * recall_neg * precision_neg) / (recall_neg + precision_neg)

    # Display confusion table 1
    print("=" * 60)
    print("Confusion table 1".center(60))
    print(("\t".join(["\t", "pos_p", "neg_p"])).center(50))
    print(("\t".join(["pos_a", "{}".format(tp), "{}".format(fn)])).center(50))
    print(("\t".join(["pos_a", "{}".format(fp), "{}".format(tn)])).center(50))

    # Display confusion table 2
    print("=" * 60)
    print("Confusion table 2".center(60))
    print(("\t".join(["\t", "pos_p", "neg_p"])).center(50))
    print(("\t".join(["pos_a", "{}".format(tp), "{}".format(fp)])).center(50))
    print(("\t".join(["pos_a", "{}".format(fn), "{}".format(tn)])).center(50))

    # Display precision, recall and f1 score
    print("=" * 60)
    print("Results".center(60))
    print("=" * 60)
    print(("\t".join(["\t", "pos", "\t", "neg"])).center(50))
    print(("\t".join(["precision", "{0:.2f}%".format(100 * precision_pos),
                      "{0:.2f}%".format(100 * precision_neg)])).center(50))
    print(("\t".join(["recall", "{0:.2f}%".format(100 * recall_pos),
                      "{0:.2f}%".format(100 * recall_neg)])).center(50))
    print(("\t".join(["f1 score", "{0:.2f}%".format(100 * f1_pos),
                      "{0:.2f}%".format(100 * f1_neg)])).center(50))


if __name__ == "__main__":
    training()
    testing()
evaluation()
