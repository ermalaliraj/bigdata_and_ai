import pandas as pd
from matplotlib import pyplot as plt

pd.options.display.width = 0
df = pd.read_csv("HR_comma_sep.csv")
print("\ndf: \n", df.head())
print("df rows x col: ", df.shape)

left = df[df.left == 1]
print("\ndf[df.left == 1]: ", left.shape)
retained = df[df.left == 0]
print("df[df.left == 0]: ", retained.shape)

"""
From above table we can draw following conclusions:
**Satisfaction Level**: seems to be relatively low (0.44) in employees leaving the firm vs the retained ones (0.66)</li>
**Average Monthly Hours**: are higher in employees leaving the firm (199 vs 207)
**Promotion Last 5 Years**: Employees who are given promotion are likely to be retained at firm.
"""

groupby = df.groupby('left').mean()
print("\ndf.groupby('left'): \n", groupby)
print("Satisfaction level of people who left is: ", groupby.iloc[1, 0])
print("Satisfaction level of people who DIDN'T left is: ", groupby.iloc[0, 0])
print("\nWork_accident of people who left is: ", groupby.iloc[1]['Work_accident'])
print("Work_accident of people who DIDN'T left is: ", groupby.iloc[0]['Work_accident'])
print("\npromotion_last_5years level of people who left is: ", groupby.iloc[1]['promotion_last_5years'])
print("promotion_last_5years level of people who DIDN'T left is: ", groupby.iloc[0]['promotion_last_5years'])

ct = pd.crosstab(df.salary, df.left)
print("\npd.crosstab(df.salary, df.left): \n", ct)
ct.plot(kind='bar')

pd.crosstab(df.Department, df.left).plot(kind='bar')

subdf = df[['satisfaction_level', 'average_montly_hours', 'promotion_last_5years', 'salary']]
print("\nsubdf: \n", subdf.head())

subdf_dummies = pd.get_dummies(subdf.salary, prefix="salary")
print("\nsubdf_dummies: \n", subdf_dummies.head())
df_with_dummies = pd.concat([subdf, subdf_dummies], axis='columns')
df_with_dummies.drop('salary', axis='columns', inplace=True)
X = df_with_dummies
print(" \n subdf_dummies as X: \n", df_with_dummies.head())

y = df.left
print("\ndf.left as y: \n", y)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.3)
model = LogisticRegression()
model.fit(X_train, y_train)

print("\nmodel.predict(X_test): ", model.predict(X_test))
print("model.score(X_test,y_test): ", model.score(X_test, y_test))

plt.show()