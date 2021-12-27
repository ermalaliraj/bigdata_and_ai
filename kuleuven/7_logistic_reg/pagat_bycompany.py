import time

import pandas as pd
from matplotlib import pyplot as plt


def groupBy_mean(df, column, value):
    df_search = df[df[column] == value]
    groupBy_df = df_search.groupby(by=[column])

    groupBy_df_sum = groupBy_df.mean()
    groupBy_df_count = groupBy_df.count()

    print("Found nr: {} of type: '{}' for value: '{}'. (avarage): {:,.2f}"
          .format(groupBy_df_count.iloc[0, 0], column, value, groupBy_df_sum.iloc[0, 0]))


def groupBy_sum(df, column, value):
    df_search = df[df[column] == value]
    groupBy_df = df_search.groupby(by=[column])

    groupBy_df_sum = groupBy_df.sum()
    groupBy_df_count = groupBy_df.count()

    print("Found nr: {} of type: '{}' for value: '{}'. (sum): {:,.2f}"
          .format(groupBy_df_count.iloc[0, 0], column, value, groupBy_df_sum.iloc[0, 0]))


def groupByCityAndSubject_count(df, city="Tiranë"):
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByCityAndSubject_count: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby(['DRT'], as_index=False)
                  .agg({'Subjekti': ['nunique']}))
    print("groupByCityAndSubject_count():\n ", groupBy_df)
    groupBy_df.plot(kind='bar', x='DRT', y='Subjekti')
    plt.xlabel('Qyteti ' + city)
    plt.ylabel('Numri i Subjekteve')
    plt.show()

def groupByCityAndProfession_count(df, city="Tiranë"):
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByCityAndProfession_count: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby(['DRT'], as_index=False)
                  .agg({'Profesioni': ['nunique']})
                  # .agg({'count': 'count'})
                  )
    groupBy_df.plot(kind='bar', x='DRT', y='Profesioni')
    plt.xlabel('Qyteti ' + city)
    plt.ylabel('Numri i Profesioneve')
    print("groupByCityAndProfession_count:\n ", groupBy_df)
    plt.show()


# def groupByProfession_count(df, city="Tiranë"):
#     df = df[df['DRT'].str.contains(city) == True]
#     print("groupByProfession_count: {} shape: {} ".format(city, df.shape))
#
#     groupBy_df = (df.groupby('DRT', as_index=False)['Profesioni']
#                   .agg({'count': 'count'})
#                   # .query('count > 4')
#                   )
#     print("groupByProfession_count():\n ", groupBy_df)
#     groupBy_df.plot(kind='bar', x='DRT', y='count')
#     plt.xlabel('Qyteti')
#     plt.ylabel('Numri i Profesioneve')
#     plt.show()


def groupByProfession_nrEmployees(df, city="Tiranë"):
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByProfession_nrEmployees: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby('Profesioni', as_index=False)['EMRI I PLOTE']
                  .agg(['count'])
                  .query('count > 4'))
    groupBy_df.plot(kind='bar')
    plt.xlabel('Profesionet ' + city)
    plt.ylabel('Numri i te punesuarve')
    plt.show()
    print("groupByProfession_nrEmployees():\n ", groupBy_df)


def groupByProfession_money(df, city="Tiranë"):
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByProfession_money: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby('Profesioni', as_index=False)['Paga Bruto']
                  .agg(['count', 'min', 'max', 'mean'])
                  .query('count > 4'))

    print("groupByProfession_money \n", groupBy_df)
    groupBy_df.plot(kind='bar')
    plt.xlabel('Profesionet ' + city)
    plt.ylabel('Te ardhurat mujore')
    plt.show()


def showProfession_money(df, city="Tiranë"):
    df = df[df['DRT'].str.contains(city) == True]
    print("city: {} shape: {} ".format(city, df.shape))


def searchInExcel(fileIn):
    time_start = time.time()
    df = pd.read_excel(fileIn)
    time_load = time.time()
    print("loaded excel file in {:,.1f} secs".format(time_load - time_start))

    groupByCityAndSubject_count(df, "")
    groupByCityAndProfession_count(df, "")
    groupByProfession_nrEmployees(df, "")
    groupByProfession_money(df, "")
    showProfession_money(df, "")


if __name__ == "__main__":
    fileIn = "janar_1cent.xlsx"
    fileOut = "out.xlsx"
    searchInExcel(fileIn)
