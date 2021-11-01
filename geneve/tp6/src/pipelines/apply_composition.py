from __future__ import print_function
'''
Created on Oct 17, 2012

@author: Georgiana Dinu, Pham The Nghia
'''

import sys
import getopt
try:
    from ConfigParser import ConfigParser # python 2
except ImportError:
    from configparser import ConfigParser # python 3
from composes.semantic_space.space import Space
from composes.composition.composition_model import CompositionModel
from composes.composition.dilation import Dilation
from composes.composition.weighted_additive import WeightedAdditive
from composes.composition.lexical_function import LexicalFunction
from composes.composition.multiplicative import Multiplicative
from composes.utils import io_utils
from composes.utils import log_utils
import pipelines.pipeline_utils as utils

import logging
logger = logging.getLogger("test vector space construction pipeline")


def usage(errno=0):
    print("""Usage:
    python apply_composition.py [options] [config_file]

    Options:
    -i --input <file>: input file.
    -o --output <dir>: output directory. Resulted composed space is output
                        in pickle format.
    -m --model <string>: model name. One of weighted_add (WeightedAdditive)
                        dilation (Dilation) or mult (Multiplicative).
    --alpha <scalar>: parameter for model=weighted_add
    --beta <scalar>: parameter for model=weighted_add
    --lambda <scalar>: parameter for model=dilation
    --load_model <file>: file containing a previously saved model. Only one of
                        --model or --load_model can be provided.
    -a --arg_space <file[,file]>: file(s) of argument semantic space (in pickle
                        format). The second word of a word pair is interpreted
                        in the second space, if provided.
    --output_format: <string> Additional output format for the resulted composed
                        space: one of sm(sparse matrix), dm(dense matrix).
                        Optional.
    -l --log <file>: log file. Optional.
    -h --help : help

    Arguments:
    config_file: <file>, used as default values for configuration options above.
            If you don't specify these options in [options] the value from the
            config_file will be used.

    Example:
    """)
    sys.exit(errno)


def create_model(model, alpha, beta, lambda_):

    #TODO: IMPORTANT here: if alpha, beta of lambda are none
    model_dict = {"weighted_add": WeightedAdditive,
                 "dilation": Dilation,
                 "mult": Multiplicative
                 }
    if not model in model_dict:
        raise ValueError("Invalid model:%s" % model)

    if model == "weighted_add":
        model_obj = WeightedAdditive(alpha, beta)
    elif model == "dilation":
        model_obj = Dilation(lambda_)
    else:
        model_obj = Multiplicative()
    return model_obj


def apply_model(in_file, out_dir, model, trained_model, arg_space_files,
                alpha, beta, lambda_, out_format):

    print("Reading in data...")
    in_descr = in_file.split("/")[-1]

    if not model is None:
        model_obj = create_model(model, alpha, beta, lambda_)
    else:
        model_obj = io_utils.load(trained_model, CompositionModel)

    model_descr = type(model_obj).__name__

    arg_space = io_utils.load(arg_space_files[0], Space)
    arg_space2 = None
    if len(arg_space_files) == 2:
        arg_space2 = io_utils.load(arg_space_files[1], Space)

    data = io_utils.read_tuple_list(in_file, fields=[0, 1, 2])

    print("Applying composition model:%s" % model_descr)
    if arg_space2 is None or type(model_obj) is LexicalFunction:
        composed_space = model_obj.compose(data, arg_space)
    else:
        composed_space = model_obj.compose(data, (arg_space, arg_space2))

    print("Printing...")
    out_file = ".".join([out_dir + "/COMPOSED_SS", model_descr, in_descr])
    io_utils.save(composed_space, "%s.pkl" % out_file)

    if not out_format is None:
        composed_space.export(out_file, format=out_format)


def main(sys_argv):
    try:
        opts, argv = getopt.getopt(sys_argv[1:], "hi:o:m:a:l:",
                                   ["help", "input=", "output=", "model=",
                                    "alpha=", "beta=", "lambda=", "arg_space=",
                                    "load_model=", "output_format=", "log="])

    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)

    out_dir = None
    in_file = None
    model = None
    arg_space = None
    trained_model = None
    alpha = None
    beta = None
    lambda_ = None
    log_file = None
    out_format = None

    section = "apply_composition"

    if (len(argv) == 1):
        config_file = argv[0]
        config = ConfigParser()
        config.read(config_file)
        out_dir = utils.config_get(section, config, "output", None)
        in_file = utils.config_get(section, config, "input", None)
        model = utils.config_get(section, config, "model", None)
        trained_model = utils.config_get(section, config, "load_model", None)
        arg_space = utils.config_get(section, config, "arg_space", None)
        if not arg_space is None:
            arg_space = arg_space.split(",")
        alpha = utils.config_get(section, config, "alpha", None)
        beta = utils.config_get(section, config, "beta", None)
        lambda_ = utils.config_get(section, config, "lambda", None)
        log_file = utils.config_get(section, config, "log", None)
        out_format = utils.config_get(section, config, "output_format", None)

    print(opts)
    for opt, val in opts:
        if opt in ("-i", "--input"):
            in_file = val
        elif opt in ("-o", "--output"):
            out_dir = val
        elif opt in ("-m", "--model"):
            model = val
        elif opt in ("-a", "--arg_space"):
            arg_space = val.split(",")
        elif opt == "--load_model":
            trained_model = val
        elif opt == "--alpha":
            alpha = val
        elif opt == "--beta":
            beta = val
        elif opt == "--lambda":
            lambda_ = val
        elif opt == "--output_format":
            out_format = val
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
    utils.assert_xor_options(model, trained_model, "(Only) one of model name (-m) or file of model object (--load_model) are required!", usage)
    utils.assert_option_not_none(arg_space, "Argument space(s) file(s) required", usage)

    if not alpha is None:
        alpha = float(alpha)
    if not beta is None:
        beta = float(beta)
    if not lambda_ is None:
        lambda_ = float(lambda_)

    apply_model(in_file, out_dir, model, trained_model, arg_space,
                alpha, beta, lambda_, out_format)


    #TODO: VERY IMPORTAT change the name of -t --trained_model
    #TI DOES NOT HAVE TO BE TRAINED BEFORE; JUST SAVED

if __name__ == '__main__':
    main(sys.argv)
