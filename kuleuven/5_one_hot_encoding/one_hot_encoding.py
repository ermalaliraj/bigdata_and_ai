import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

df = pd.read_csv("homeprices.csv")
print("df: \n", df)

dummies = pd.get_dummies(df.town)
print("\ntown dummies: \n", dummies)

final = pd.concat([df, dummies], axis='columns')
final = final.drop(['town'], axis='columns')
final = final.drop(['west windsor'], axis='columns')  # drop 1 dummy column can be implicitly deduced
print("\nfinal df with dummies: \n", final)

X = final.drop('price', axis='columns')
y = final.price
print("\nX: \n", X)
print("\ny: \n", y)

model = LinearRegression()
model.fit(X, y)
print("\nscore : {}".format(model.score(X, y)))
print("predict 2600 sqr ft home in new jersey : {}".format(model.predict([[2800, 0, 1]])))
print("predict 3400 sqr ft home in new jersey : {}".format(model.predict([[3400, 0, 0]])))

# One Hot Encoder
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
dfle = df
dfle.town = le.fit_transform(dfle.town)
print("\ndf LabelEncoder: \n", dfle)

X = dfle[['town', 'area']].values
y = dfle.price
print("\nX: \n", X)
print("\ny: \n", y)

from sklearn.preprocessing import OneHotEncoder
# ohe = OneHotEncoder([('one_hot_encoder', OneHotEncoder(), [0])], remainder='passthrough')
# X = ohe.fit_transform(X).toarray()
onehotencoder = ColumnTransformer([("town", OneHotEncoder(), [0])], remainder="passthrough")
X = onehotencoder.fit_transform(X)
print("\nX OneHotEncoder: \n", X)

X = X[:, 1:]
print("\nX OneHotEncoder - first column: \n", X)

model.fit(X, y)
print("\nscore : {}".format(model.score(X, y)))
print("predict 2600 sqr ft home in new jersey : {}".format(model.predict([[1, 0, 2800]])))
print("predict 3400 sqr ft home in new jersey : {}".format(model.predict([[0, 1, 3400]])))