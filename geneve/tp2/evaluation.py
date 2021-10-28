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
