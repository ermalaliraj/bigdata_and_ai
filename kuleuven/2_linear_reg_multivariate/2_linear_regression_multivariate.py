import math

import pandas as pd
from sklearn import linear_model

df = pd.read_csv('homeprices.csv')
print("df: \n", df)

median_bedroom = math.floor(df.bedrooms.median())
print("median_bedroom: \n", median_bedroom)
df.bedrooms = df.bedrooms.fillna(median_bedroom)
print("df filledna: \n", df)

# plt.xlabel('area')
# plt.ylabel('price')
# plt.scatter(df.area, df.price, color='red', marker='+')
# plt.show()
#
# new_df = df.drop('price', axis='columns')
# print("new_df: \n", new_df)
#
# price = df.price
# print("price: \n", price)
#
reg = linear_model.LinearRegression()
reg.fit(df[['area', 'bedrooms', 'age']], df.price)
print("\nreg.coef_:", reg.coef_)
print("reg.intercept_:", reg.intercept_)

predict = reg.predict([[3000, 3, 40]])
print("predict area_3000 bedrooms_3 age_40: ", predict)  # 498408 how was calculated?
# predict = reg.predict([[3000, 3, 15]])
# print("predict 3000 3 15: ", predict)

price = 112.06244194 * 3000 + 23388.88007794 * 3 + -3231.71790863 * 40 + 221323.00186540443
print("price (coef1*area + coef2*bedrooms + coef3*age + intercept): ", price)

predict = reg.predict([[2500, 5, 5]])
print("predict area_3000 bedrooms_5 age_5: ", predict)


#
# area_df = pd.read_csv("areas.csv")
# area_df.head(3)
# print("\narea_df.head(3): \n", area_df.head(3))
#
# p = reg.predict(area_df)
# print("\np: ", p)
#
# area_df['prices'] = p
#
# print("\narea_df: \n", area_df)
# area_df.to_csv("prediction.csv")
