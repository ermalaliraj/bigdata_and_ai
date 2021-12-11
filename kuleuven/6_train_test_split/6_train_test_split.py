import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot(xLabel, x, yLabel, y, printLine=False):
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.scatter(x, y, color='red', marker='+')
    if printLine:
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b)
    plt.show()


df = pd.read_csv("carprices.csv")
print("\ndf: \n", df.head())
print("df rows x col: ", df.shape)

plot('Mileage', df['Mileage'], 'Sell Price($)', df['Sell Price($)'], True)
plot('Age(yrs)', df['Age(yrs)'], 'Sell Price($)', df['Sell Price($)'], True)

X = df[['Mileage', 'Age(yrs)']]
y = df['Sell Price($)']
print("\nX: \n", X.head())
print("\ny: \n", y.head())

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print("\nX_train: ", len(X_train))
print("X_test: ", len(X_test))
print("y_train: ", len(y_train))
print("y_test: ", len(y_test))

from sklearn.linear_model import LinearRegression
clf = LinearRegression()
clf.fit(X_train, y_train)

print("\nclf.predict(X_test): ", clf.predict(X_test))
print("clf.score(X_test, y_test): ", clf.score(X_test, y_test))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)  # always fix train data
clf = LinearRegression()
clf.fit(X_train, y_train)
print("\nclf.predict(X_test): ", clf.predict(X_test))
print("clf.score(X_test, y_test): ", clf.score(X_test, y_test))
