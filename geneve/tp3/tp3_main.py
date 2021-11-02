from geneve.tp3.countfreqs import countNgrams
from geneve.tp3.evaltagger import corpus_iterator, Evaluator
from geneve.tp3.tp3_ex1_p1p2 import create_rare_emission_file
from geneve.tp3.tp3_ex1_p3 import tagger

if __name__ == "__main__":
    geneFileName = "./doc/gene.key"
    geneCountsFileName = "./doc/gene.key.counts"

    geneFile = open(geneFileName, "r")
    geneCountsFile = open(geneCountsFileName, "w")  # sys.stdout

    # Count Words and creates .counts file
    countNgrams(geneFile, 3, geneCountsFile)  # creates .counts file

    create_rare_emission_file(geneCountsFileName, geneFileName)  # creates gene.train.rare file

    tagger(geneCountsFileName, geneFileName)

    keyFile = "./doc/gene.key"
    prediction_file = "./doc/gene.key.p1.out"
    gs_iterator = corpus_iterator(open(keyFile))
    pred_iterator = corpus_iterator(open(prediction_file))
    evaluator = Evaluator()
    evaluator.compare(gs_iterator, pred_iterator)
    evaluator.print_scores()
