import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sn

digits = load_digits()

plt.gray()
for i in range(5):
    # plt.matshow(digits.images[i])
    print("digits.images[{}]: {}\n".format(i, digits.images[i]))

print("dir(digits): ", dir(digits))
print("DESCR: ", digits.DESCR[:100])
print("len(data): ", len(digits.data))
print("feature_names: ", digits.feature_names)
print("frame: ", digits.frame)
print("len(images): ", len(digits.images))
print("target: ", digits.target)
print("len(target): ", len(digits.target))
print("target_names: ", digits.target_names)

model = LogisticRegression()
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2)
model.fit(X_train, y_train)

print("\nmodel.score(X_test, y_test): ", model.score(X_test, y_test))
print("model.predict(digits.data[0:5]): ", model.predict(digits.data[0:5]))

print("\nX_test to predict: \n", X_test)
y_predicted = model.predict(X_test)
print("model.predict(X_test): \n", model.predict(X_test))

cm = confusion_matrix(y_test, y_predicted)
print("\ncm: \n", cm)

plt.figure(figsize = (10,7))
sn.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')

plt.show()
