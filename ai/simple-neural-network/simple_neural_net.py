import numpy as np


# sigmoid function to normalize inputs
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# sigmoid derivatives to adjust synaptic weights
def sigmoid_derivative(x):
    return x * (1 - x)


training_inputs = np.array([[0, 0, 1],
                            [1, 1, 1],
                            [1, 0, 1],
                            [0, 1, 1]])

# output dataset
training_outputs = np.array([[0, 1, 1, 0]]).T

# seed random numbers to make calculation
np.random.seed(1)
synaptic_weights = 2 * np.random.random((3, 1)) - 1
# [[-0.16595599]
#  [ 0.44064899]
#  [-0.99977125]]

print('Random starting synaptic weights')
print(synaptic_weights)

for iteration in range(20000):
    input_layer = training_inputs

    # Normalize the product of the input layer with the synaptic weights
    output = sigmoid(np.dot(input_layer, synaptic_weights))
    # [[0.2689864 ]
    #  [0.3262757 ]
    #  [0.23762817]
    #  [0.36375058]]
    #  Formula: x1*w1 + x2*w2 + x3*w3
    #  0*-0,165 + 0*0,440 + 1*-0,999 = -0,999
    # if we pass this  -0,999 to the sigmoid normalization gives 0,2689864

    # how much did we miss?
    error = training_outputs - output
    # multiply how much we missed by the slope of the sigmoid at the values in outputs
    adjustments = error * sigmoid_derivative(output)
    # update weights
    synaptic_weights += np.dot(input_layer.T, adjustments)

print('Synaptic weight after training')
print(synaptic_weights)

print('Output after training')
print(output)
