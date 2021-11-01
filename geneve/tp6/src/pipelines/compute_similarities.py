from __future__ import print_function
'''
Created on Oct 17, 2012

@author: Georgiana Dinu, Pham The Nghia
'''
'''
Created on Oct 17, 2012

@author: Georgiana Dinu, Pham The Nghia
'''

'''
Created on Jun 12, 2012

@author: thenghia.pham
'''


import sys
import os
import getopt
from warnings import warn
try:
    from ConfigParser import ConfigParser # python 2
except ImportError:
    from configparser import ConfigParser # python 3
from composes.semantic_space.space import Space
from composes.similarity.cos import CosSimilarity
from composes.similarity.lin import LinSimilarity
from composes.similarity.dot_prod import DotProdSimilarity
from composes.similarity.euclidean import EuclideanSimilarity
from composes.utils import io_utils
from composes.utils import log_utils
import pipelines.pipeline_utils as utils

import logging
logger = logging.getLogger("test vector space construction pipeline")


def usage(errno=0):
    print("""Usage:
    python compute_similarities.py [options] [config_file]

    Options:
    -i --input <file>: input file.
    -o --output <dir>: output directory.
    -s --space <file[,file2]>: file of semantic space. The second
            word of a word pair is interpreted in the second space argument,
            if provided.
    --in_dir: <dir>: input directory for the semantic spaces, all files are loaded
                one at a time and -s value is ignored. Optional.
    -m --sim_measure <list(string)>: comma-separated similarity measures
    -c --columns <(int,int)>: pair of columns, indicating which columns contain
            the words to be compared
    -l --log <file>: log file. Optional, default ./build_core_space.log
    -h --help : help

    Arguments:
    config_file: <file>, used as default values for configuration options above.
            If you don't specify these options in [options] the value from the
            config_file will be used.

    Example:
    """)
    sys.exit(errno)


def compute_sim_batch(in_file, columns, out_dir, sim_measures, in_dir):

    if not os.path.exists(in_dir):
        raise ValueError("Input directory not found: %s" % in_dir)

    if not in_dir.endswith("/"):
        in_dir = in_dir + "/"

    for file_ in os.listdir(in_dir):
        if file_.endswith(".pkl"):
            space_file = in_dir + file_

            print(space_file)
            compute_sim(in_file, columns, out_dir, sim_measures, [space_file])


def compute_sim(in_file, columns, out_dir, sim_measures, space_files):

    sim_dict = {"cos": CosSimilarity(),
                "lin": LinSimilarity(),
                "dot_prod": DotProdSimilarity(),
                "euclidean": EuclideanSimilarity()}

    if not len(columns) == 2:
        raise ValueError("Column description unrecognized!")
    col0 = int(columns[0]) - 1
    col1 = int(columns[1]) - 1

    try:
        space = io_utils.load(space_files[0], Space)
    except TypeError:
        warn("Not a Space instance in file: %s" % space_files[0])
        return

    space2 = None
    space_descr = ".".join(space_files[0].split("/")[-1].split(".")[0:-1])

    if len(space_files) == 2:
        space2 = io_utils.load(space_files[1], Space)
        space_descr = ".".join([space_descr] + space_files[1].split("/")[-1].split(".")[0:-1])

    descr = ".".join(["SIMS", in_file.split("/")[-1], space_descr])

    for sim_measure in sim_measures:
        print("Computing similarities: %s" % sim_measure)
        if not sim_measure in sim_dict:
            warn("Similarity measure:%s not defined" % sim_measure)
            continue

        sim = sim_dict[sim_measure]
        out_file = '%s/%s.%s' % (out_dir, descr, sim_measure)
        io_utils.create_parent_directories(out_file)

        with open(in_file) as in_stream, open(out_file,"w") as out_stream:
            for line in in_stream:
                if not line.strip() == "":
                    elems = line.strip().split()
                    word1 = elems[col0]
                    word2 = elems[col1]

                    predicted_sim = space.get_sim(word1, word2, sim, space2)
                    out_stream.write("%s %s\n" % (line.strip(), str(predicted_sim)))


def main(sys_argv):
    try:
        opts, argv = getopt.getopt(sys_argv[1:], "hi:o:s:m:c:l:",
                                   ["help", "input=", "output=", "sim_measures=",
                                    "space=", "in_dir=", "columns=", "log=" ])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)


    out_dir = None
    in_file = None
    sim_measures = None
    spaces = None
    columns = None
    log_file = None
    in_dir = None
    section = "compute_similarities"

    if (len(argv) == 1):
        config_file = argv[0]
        config = ConfigParser()
        config.read(config_file)
        out_dir = utils.config_get(section, config, "output", None)
        in_file = utils.config_get(section, config, "input", None)
        in_dir = utils.config_get(section, config, "in_dir", None)
        sim_measures = utils.config_get(section, config, "sim_measures", None)
        if not sim_measures is None:
            sim_measures = sim_measures.split(",")
        spaces = utils.config_get(section, config, "space", None)
        if not spaces is None:
            spaces = spaces.split(",")
        columns = utils.config_get(section, config, "columns", None)
        if not columns is None:
            columns = columns.split(",")
        log_file = utils.config_get(section, config, "log", None)

    for opt, val in opts:
        if opt in ("-i", "--input"):
            in_file = val
        elif opt in ("-o", "--output"):
            out_dir = val
        elif opt == ("--in_dir"):
            in_dir = val
        elif opt in ("-m", "--sim_measures"):
            sim_measures = val.split(",")
        elif opt in ("-s", "--space"):
            spaces = val.split(",")
        elif opt in ("-c", "--columns"):
            columns = val.split(",")
        elif opt in ("-l", "--log"):
            log_file = val
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            usage(1)

    log_utils.config_logging(log_file)

    utils.assert_option_not_none(in_file, "Input file required", usage)
    utils.assert_option_not_none(out_dir, "Output directory required", usage)
    utils.assert_option_not_none(sim_measures, "Similarity measures required", usage)
    utils.assert_option_not_none(columns, "Columns to be read from input file required", usage)

    if not in_dir is None:
        compute_sim_batch(in_file, columns, out_dir, sim_measures, in_dir)
    else:
        utils.assert_option_not_none(spaces, "Semantic space file required", usage)
        compute_sim(in_file, columns, out_dir, sim_measures, spaces)


if __name__ == '__main__':
    main(sys.argv)
