#ex13.py
#-------
from composes.utils import io_utils
from composes.composition.weighted_additive import WeightedAdditive


#training data
train_data = [("good", "car", "good_car"),
              ("good", "book", "good_book")
              ]

#load an argument space
arg_space = io_utils.load("./data/out/ex10.pkl")
print arg_space.id2row
print arg_space.cooccurrence_matrix

#load a phrase space
phrase_space = io_utils.load("data/out/PHRASE_SS.ex10.pkl")
print phrase_space.id2row
print phrase_space.cooccurrence_matrix

#train a weighted additive model on the data
my_comp = WeightedAdditive()
my_comp.train(train_data, arg_space, phrase_space)

#print its parameters
print "alpha:", my_comp.alpha
print "beta:", my_comp.beta



