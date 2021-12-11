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


df = pd.read_csv("insurance_data.csv")
print("\ndf: \n", df.head())
print("df rows x col: ", df.shape)

plot('Age', df.age, 'bought_insurance', df.bought_insurance, True)

X_train, X_test, y_train, y_test = train_test_split(df[['age']], df.bought_insurance, train_size=0.8)
print("\nX_test: \n", X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

print("\nmodel.predict(X_test): ", model.predict(X_test))
print("model.score(X_test, y_test): ", model.score(X_test, y_test))
print("model.predict_proba(X_test): \n", model.predict_proba(X_test))
