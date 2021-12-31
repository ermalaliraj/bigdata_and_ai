import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("titanic.csv")
print("df: \n", df.head())
print("df rows x col: ", df.shape)

inputs = df.drop('salary_more_then_100k', axis='columns')
target = df['salary_more_then_100k']
print("inputs: \n", inputs)

le_company = LabelEncoder()
le_job = LabelEncoder()
le_degree = LabelEncoder()
inputs['company_n'] = le_company.fit_transform(inputs['company'])
inputs['job_n'] = le_job.fit_transform(inputs['job'])
inputs['degree_n'] = le_degree.fit_transform(inputs['degree'])
print("inputs with LabelEncoder: \n", inputs)

inputs_n = inputs.drop(['company', 'job', 'degree'], axis='columns')
print("inputs normalized: \n", inputs_n)
print("target: \n", target)

model = tree.DecisionTreeClassifier()
model.fit(inputs_n, target)

print("\nmodel.score(inputs_n,target): ", model.score(inputs_n, target))

print("\nIs salary of Google, Computer Engineer, Bachelors degree > 100 k ?: ", model.predict([[2, 1, 0]]))
print("Is salary of Google, Computer Engineer, Master degree > 100 k ?: ", model.predict([[2, 1, 1]]))

# print("\nle_company.inverse_transform(target): \n", le_company.inverse_transform(target))
# print("\nle_job.inverse_transform(target): \n", le_job.inverse_transform(target))
# print("\nle_degree.inverse_transform(target): \n", le_degree.inverse_transform(target))