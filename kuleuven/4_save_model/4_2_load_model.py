import pickle

with open('model_pickle', 'rb') as f:
    model = pickle.load(f)

print("\npredict area 5000 with pickle model: ", model.predict([[5000]]))


# for huge numpy arrays models use joblib
import joblib
model = joblib.load('model_joblib')
print("\npredict area 5000 with joblib model: ", model.predict([[5000]]))
