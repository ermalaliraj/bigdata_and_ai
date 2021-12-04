import math
import pandas as pd
from sklearn import linear_model
from word2number import w2n

df = pd.read_csv("hiring.csv")
print("df: \n", df)

# Handling NA values
df.experience = df.experience.fillna("zero")
df['test_score(out of 10)'] = df['test_score(out of 10)'].fillna(math.floor(df['test_score(out of 10)'].median()))
df.experience = df.experience.apply(w2n.word_to_num)
print("\ndf handled NA values, normalised to integers: \n", df)

reg = linear_model.LinearRegression()
reg.fit(df[['experience', 'test_score(out of 10)', 'interview_score(out of 10)']], df['salary($)'])
print("\nCoefficients:", reg.coef_)
print("Intercept:", reg.intercept_)

predictCheck = reg.coef_[0] * 2 + reg.coef_[1] * 9 + reg.coef_[2] * 6 + reg.intercept_
print("\npredict 2 years of experience, 9 test scores, 6 interview scores: ", reg.predict([[2, 9, 6]]))
print("predictCheck (reg.coef_[0] * 2 + reg.coef_[1] * 9 + reg.coef_[2] * 6 + reg.intercept_): ", predictCheck)

print("\npredict 12 years of experience, 10 test scores, 10 interview scores: ", reg.predict([[12, 10, 10]]))
print("predict 0 years of experience, 10 test scores, 10 interview scores: ", reg.predict([[0, 10, 10]]))
print("predict 1  years of experience, 9  test scores, 6  interview scores: ", reg.predict([[1, 9, 6]]))
print("predict 10 years of experience, 9  test scores, 6  interview scores: ", reg.predict([[10, 9, 6]]))
print("predict 0  years of experience, 0  test scores, 0  interview scores: ", reg.predict([[0, 0, 0]]))
print("predict 5  years of experience, 0  test scores, 0  interview scores: ", reg.predict([[5, 0, 0]]))
print("predict 10 years of experience, 0  test scores, 0  interview scores: ", reg.predict([[10, 0, 0]]))
