import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

pd.options.display.width = 0
df = pd.read_csv("salaries.csv")
print("df: \n", df.head())
print("df rows x col: ", df.shape)

le_company = LabelEncoder()
le_job = LabelEncoder()
le_degree = LabelEncoder()
df['company_n'] = le_company.fit_transform(df['company'])
df['job_n'] = le_job.fit_transform(df['job'])
df['degree_n'] = le_degree.fit_transform(df['degree'])
print("\ndf with LabelEncoder: \n", df)

inputs_n = df.drop(['company', 'job', 'degree'], axis='columns')
print("\ndf normalized (text col): \n", inputs_n)
inputs_n = inputs_n.drop('salary_more_then_100k', axis='columns')
target = df['salary_more_then_100k']
print("\ninputs_n: (to be found salary_more_then_100k value)\n", inputs_n)
# print("target: \n", target)

model = tree.DecisionTreeClassifier()
model.fit(inputs_n, target)

print("\nmodel.score(inputs_n,target): ", model.score(inputs_n, target))

print("\nIs salary of Google, Computer Engineer, Bachelors degree > 100 k ?: [2, 1, 0]: ", model.predict([[2, 1, 0]]))
print("Is salary of Google, Computer Engineer, Master degree > 100 k ?: [2, 1, 1]: ", model.predict([[2, 1, 1]]))

# print("\nle_company.inverse_transform(target): \n", le_company.inverse_transform(target))
# print("\nle_job.inverse_transform(target): \n", le_job.inverse_transform(target))
# print("\nle_degree.inverse_transform(target): \n", le_degree.inverse_transform(target))