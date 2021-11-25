import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

df = pd.read_csv('homeprices.csv')
print("df: \n", df)

plt.xlabel('area')
plt.ylabel('price')
plt.scatter(df.area, df.price, color='red', marker='+')
plt.show()

new_df = df.drop('price', axis='columns')
print("new_df: \n", new_df)

price = df.price
print("price: \n", price)

reg = linear_model.LinearRegression()
reg.fit(new_df, price)

reg.predict([[3300]])
print("\nreg.coef_:", reg.coef_)
print("reg.intercept_:", reg.intercept_)

a = 3300*135.78767123 + 180616.43835616432
print("area: ", a)

print("reg.predict([[5000]]): ", reg.predict([[5000]]))

area_df = pd.read_csv("areas.csv")
area_df.head(3)
print("\narea_df.head(3): \n", area_df.head(3))

p = reg.predict(area_df)
print("\np: ", p)

area_df['prices'] = p

print("\narea_df: \n", area_df)
area_df.to_csv("prediction.csv")
