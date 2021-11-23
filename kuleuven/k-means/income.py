import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def plot():
    df1 = df[df.cluster == 0]
    df2 = df[df.cluster == 1]
    df3 = df[df.cluster == 2]
    # print("df cluster==0\n", df1.head())
    # print("df cluster==1\n", df1.head())
    # print("df cluster==2\n", df1.head())
    # print("df cluster km.cluster_centers_\n", km.cluster_centers_)
    plt.scatter(df1.Age, df1['Income'], color='green')
    plt.scatter(df2.Age, df2['Income'], color='red')
    plt.scatter(df3.Age, df3['Income'], color='black')
    # plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')
    plt.xlabel('Age')
    plt.ylabel('Income')
    # plt.hist(['Age', 'Income']
    #          , color=["lightcoral"]
    #          , stacked=True,
    #          label=['Age', 'Income'])
    # plt.legend()
    plt.show()

# Import CVS
df = pd.read_csv("income.csv", delimiter=';')
print("df original: \n", df, "\n")

# Create KMeans Plot
km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['Age', 'Income']])
print("clusters predicted: ", y_predicted)
df['cluster'] = y_predicted
print("df with cluster column: \n", df)
# plot()

# Normalize Age and Income in the scale 0-1
scaler = MinMaxScaler()
df['Income'] = scaler.fit_transform(df[['Income']])
scaler.fit(df[['Age']])
df.Age = scaler.transform(df[['Age']])
print("\ndf MinMaxScaler on Income and Age: \n", df)
# plot()

# Fit another time
y_predicted = km.fit_predict(df[['Age', 'Income']])
df['cluster'] = y_predicted  # override column 'cluster', no need to drop
print("\nFinal df after second prediction: \n", df)

plot()

k_rng = range(1, 10)
sse = []
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df[['Age', 'Income']])
    sse.append(km.inertia_)  # Sum up sum error
print("Sum of Squared error: \n", sse)

# Plot to check where is the Elbow. Will be at number 3
plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng, sse)
plt.show()
