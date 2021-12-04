import pickle

import pandas as pd
from sklearn import linear_model

df = pd.read_csv("homeprices.csv")
print("\ndf:", df.head())

model = linear_model.LinearRegression()
model.fit(df[['area']], df.price)

print("\nCoefficients:", model.coef_)
print("Intercept:", model.intercept_)

print("\npredict area 5000: ", model.predict([[5000]]))

with open('model_pickle', 'wb') as f:
    pickle.dump(model, f)

# for huge numpy arrays models use joblib
import joblib
joblib.dump(model, 'model_joblib')
