import math

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

df = pd.read_csv('homeprices.csv')
print("df: \n", df)

# Handling NA values
median_bedroom = math.floor(df.bedrooms.median())
print("\nmedian for bedrooms:", median_bedroom)
print("median for area:", math.floor(df.area.median()))
print("median for age:", math.floor(df.age.median()))
df.bedrooms = df.bedrooms.fillna(median_bedroom)
print("\ndf filled_na with median: \n", df)

# plt.xlabel('area')
# plt.ylabel('price')
# plt.scatter(df.area, df.price, color='red', marker='+')
# plt.scatter(df.area, df.bedrooms, color='blue', marker='*')
# plt.scatter(df.area, df.age, color='purple', marker='+')
# plt.show()

reg = linear_model.LinearRegression()
reg.fit(df[['area', 'bedrooms', 'age']], df.price)
print("\nCoefficients:", reg.coef_)
print("Intercept:", reg.intercept_)

predict = reg.predict([[3000, 3, 40]])
print("\npredict area_3000 bedrooms_3 age_40: ", predict)  # 498408 how was calculated?
price = 112.06244194 * 3000 + 23388.88007794 * 3 + -3231.71790863 * 40 + 221323.00186540443
print("price (coef1*area + coef2*bedrooms + coef3*age + intercept): ", price)
price = reg.coef_[0] * 3000 + reg.coef_[1] * 3 + reg.coef_[2] * 40 + reg.intercept_
print("price (reg.coef_[0] * 3000 + reg.coef_[1] * 3 + reg.coef_[2] * 40 + reg.intercept_): ", price)

print("\npredict area_3000 bedrooms_3 age_15: ", reg.predict([[3000, 3, 15]]))
print("predict area_3000 bedrooms_5 age_5: ", reg.predict([[2500, 5, 5]]))

print("\npredict area_3000 bedrooms_1 age_15: ", reg.predict([[3000, 1, 15]]))
print("predict area_3000 bedrooms_2 age_15: ", reg.predict([[3000, 2, 15]]))
print("predict area_3000 bedrooms_3 age_15: ", reg.predict([[3000, 3, 15]]))
print("predict area_3000 bedrooms_5 age_15: ", reg.predict([[3000, 5, 15]]))
print("predict area_3000 bedrooms_8 age_15: ", reg.predict([[3000, 8, 15]]))

print("\npredict area_3000 bedrooms_1 age_30: ", reg.predict([[3000, 1, 30]]))
print("predict area_3000 bedrooms_2 age_30: ", reg.predict([[3000, 2, 30]]))
print("predict area_3000 bedrooms_3 age_30: ", reg.predict([[3000, 3, 30]]))
print("predict area_3000 bedrooms_5 age_30: ", reg.predict([[3000, 5, 30]]))
print("predict area_3000 bedrooms_8 age_30: ", reg.predict([[3000, 8, 30]]))