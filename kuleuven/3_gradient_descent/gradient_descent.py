import matplotlib.pyplot as plt
import numpy as np


def gradient_descent(x, y):
    m_curr = b_curr = 0
    iterations = 10_000
    n = len(x)
    learning_rate = 0.08  # start from 0.00001 and increase slowly
    plt.scatter(x, y, color='red', marker='+', linewidths=5)
    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        mse_cost = (1 / n) * sum([val ** 2 for val in (y - y_predicted)])
        plt.plot(x, y_predicted, color='green')
        md = -(2 / n) * sum(x * (y - y_predicted))  # m derivative
        bd = -(2 / n) * sum(y - y_predicted)  # b derivative

        m_curr = m_curr - learning_rate * md
        b_curr = b_curr - learning_rate * bd
        print("m {}, b {}, mse_cost {} iteration {}".format(m_curr, b_curr, mse_cost, i))

    plt.show()


x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 7, 9, 11, 13])

gradient_descent(x, y)
