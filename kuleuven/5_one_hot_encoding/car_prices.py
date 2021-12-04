import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def plot(x, y, printLine=False):
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.scatter(x, y, color='red', marker='+')
    if printLine:
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m * x + b)
    plt.show()


df = pd.read_csv("carprices.csv")
print("df: \n", df)

dummies = pd.get_dummies(df['Car Model'])
print("\nCar Model dummies: \n", dummies)

final = pd.concat([df, dummies], axis='columns')
final = final.drop(['Car Model'], axis='columns')
final = final.drop(['Mercedez Benz C class'], axis='columns')  # drop 1 dummy column can be implicitly deduced
print("\nfinal df with dummies: \n", final)

X = final.drop('Sell Price($)', axis='columns')
y = final['Sell Price($)']
print("\nX: \n", X)
print("\ny: \n", y)

plot(X['Mileage'], y, True)

model = LinearRegression()
model.fit(X, y)
print("\nscore : {}".format(model.score(X, y)))
print("Predict price of a Mercedez benz that is 4 yr old mileage 45000: {}".format(model.predict([[45000, 4, 0, 0]])))
print("Predict price of a BMW X5 benz that is 7 yr old mileage 86000: {}".format(model.predict([[86000, 7, 0, 1]])))
