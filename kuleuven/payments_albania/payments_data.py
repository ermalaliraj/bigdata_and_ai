import time

import pandas as pd
from matplotlib import pyplot as plt

pathPlot = "./plot/"


def setPlot():
    ""
    # plt.rcParams['figure.figsize'] = [10, 10]  # for square canvas
    # plt.rcParams['figure.subplot.left'] = 0
    # plt.rcParams['figure.subplot.bottom'] = 0
    # plt.rcParams['figure.subplot.right'] = 1
    # plt.rcParams['figure.subplot.top'] = 1


def getITSubjects(df):
    val = ["Administrator baze të dhënash", "Administrator i sistemeve kompjuterike",
           "Administrator rrjeti",
           "Administrator sistemesh", "Administrator të dhënash", "Administrues i", "rrjeteve sociale",
           "Analist baza të dhënash", "Analist i bazës së të dhënave në sisteme", "informatike", "Analist i rrjetit",
           "Analist i sistemeve informatike të biznesit", "Analisti", "programues", "Arkitekt, baze të dhënash",
           "Arkitekt, website", "Asistent i bazës së të dhënave", "kompjuterike", "Asistent inxhinieri kompjuterike",
           "Asistent komunikimesh kompjuterike", "Asistent sistemesh kompjuterike", "Asistent, programim kompjuteri",
           "Informatikan", "Inxhinier", "informatikan", "Inxhinier softuer", "Manaxher për zhvillim aplikacionesh",
           "Programues", "Programues kompjuteri", "Programues softueri", "Programues/bazë të dhënash",
           "Projektuesi softuer",
           "Specialist i rrjetit kompjuterik", "Webmaster", "Zhvillues softuer"]
    df = df[df['Profesioni'].isin(val) == True].reset_index()
    del df['index']
    return df


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


def groupByCityAndSubject_count(df, city="Tiranë", show=True):
    # setPlot()
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByCityAndSubject_count: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby(['DRT'], as_index=False)
                  .agg({'Subjekti': ['nunique']}))
    print("groupByCityAndSubject_count():/n ", groupBy_df)
    groupBy_df.plot(kind='bar', x='DRT', y='Subjekti')
    plt.xlabel('Qyteti ' + city)
    plt.ylabel('Numri i Subjekteve')
    if show: plt.show()
    plt.savefig(pathPlot + "1.nr_subjekteve_{}.png".format(city))


def groupByCityAndProfession_count(df, city="Tiranë", show=True):
    # setPlot()
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByCityAndProfession_count: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby(['DRT'], as_index=False)
                  .agg({'Profesioni': ['nunique']})
                  # .agg({'count': 'count'})
                  )
    groupBy_df.plot(kind='bar', x='DRT', y='Profesioni')
    plt.xlabel('Qyteti ' + city)
    plt.ylabel('Numri i Profesioneve')
    print("groupByCityAndProfession_count:/n ", groupBy_df)
    if show: plt.show()
    plt.savefig(pathPlot + "2.nr_profesioneve{}.png".format(city))


def groupByProfession_nrEmployees(df, city="Tiranë", show=True):
    # setPlot()
    pngName = pathPlot + "3.nr_punesuarve_{}".format(city)

    df = df[df['DRT'].str.contains(city) == True]

    df = getITSubjects(df)
    pngName = pngName + "_IT"

    print("groupByProfession_nrEmployees: {} shape: {} ".format(city, df.shape))

    groupBy_df = (df.groupby('Profesioni', as_index=False)['EMRI I PLOTE']
                  .agg(['count']))
    groupBy_df.plot(kind='bar')
    plt.xlabel('Profesionet ' + city)
    plt.ylabel('Numri i te punesuarve')
    plt.savefig(pngName + ".png")
    if show: plt.show()
    print("groupByProfession_nrEmployees():/n ", groupBy_df)


def groupByProfession_money(df, city="Tiranë", show=True):
    # setPlot()

    df = df[df['DRT'].str.contains(city) == True]
    print("groupByProfession_money: {} shape: {} ".format(city, df.shape))

    # df = df[df['Profesioni'].str.contains("Administrator") == False].reset_index()
    val = ["Administrator", "Papercaktuar", "Drejtor në departamente të radio-televizioneve"]
    df = df[df['Profesioni'].isin(val) == False].reset_index()
    del df['index']

    groupBy_df = (df.groupby('Profesioni', as_index=False)['Paga Bruto']
                  .agg(['min', 'max', 'mean'])
                  .query('mean > 200000'))

    print("groupByProfession_money /n", groupBy_df)
    groupBy_df.plot(kind='bar')
    plt.xlabel('Profesionet ' + city + ' (mean > 200000 - no Administrators)')
    plt.ylabel('Te ardhurat mujore')
    if show: plt.show()
    plt.savefig(pathPlot + "4.te_ardhurat_2M_{}.png".format(city))


def showProfession_money(df, city="Tiranë", show=True):
    # setPlot()
    df = df[df['DRT'].str.contains(city) == True]
    print("groupByProfession_money: {} shape: {} ".format(city, df.shape))

    df = getITSubjects(df)

    groupBy_df = (df.groupby('Profesioni', as_index=False)['Paga Bruto']
                  .agg(['min', 'max', 'mean']))

    print("showProfession_money /n", groupBy_df)
    groupBy_df.plot(kind='bar')
    plt.xlabel('Profesionet ' + city)
    plt.ylabel('Te ardhurat mujore')
    if show: plt.show()
    plt.savefig(pathPlot + "5.te_ardhurat_IT_{}.png".format(city))


def searchInExcel(fileIn):
    time_start = time.time()
    df = pd.read_excel(fileIn)
    time_load = time.time()
    print("loaded excel file in {:,.1f} secs".format(time_load - time_start))

    groupByCityAndSubject_count(df, "", show=True)
    groupByCityAndProfession_count(df, "", show=True)
    groupByProfession_nrEmployees(df, show=True)
    groupByProfession_money(df, show=True)
    showProfession_money(df, show=True)


if __name__ == "__main__":
    fileIn = "C:/Users/admin/Documents/Projects/accademic/python/bigdata_and_ai/kuleuven/7_logistic_reg/janar_1cent.xlsx"
    searchInExcel(fileIn)
