import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def plot(xLabel, x, yLabel, y, printLine=False):
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.scatter(x, y, color='red', marker='+')
    if printLine:
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b)
    plt.show()


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def prediction_function(age):
    z = 0.042 * age - 1.53  # 0.04150133 ~ 0.042 and -1.52726963 ~ -1.53
    y = sigmoid(z)
    return y


df = pd.read_csv("insurance_data.csv")
print("\ndf: \n", df.head())
print("df rows x col: ", df.shape)

plot('Age', df.age, 'bought_insurance', df.bought_insurance, True)

X_train, X_test, y_train, y_test = train_test_split(df[['age']], df.bought_insurance, train_size=0.8)
print("\nX_test: \n", X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

print("model.predict(X_test): ", model.predict(X_test))
print("\nmodel.score(X_test, y_test)  (accuracy): ", model.score(X_test, y_test))
print("model.predict_proba(X_test): \n", model.predict_proba(X_test))

print("\nmodel.coef_: ", model.coef_)  # indicates value of m in y=m*x + b equation
print("model.intercept_: ", model.intercept_)  # indicates value of b in y=m*x + b equation

print("\nprediction_function(20): ", prediction_function(20))
print("prediction_function(35): ", prediction_function(35))
print("prediction_function(50): ", prediction_function(50))
print("prediction_function(70): ", prediction_function(70))
print("prediction_function(90): ", prediction_function(90))
