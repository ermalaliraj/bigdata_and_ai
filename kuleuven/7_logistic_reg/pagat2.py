import time

import pandas as pd

def searchInExcel(fileIn, fileOut, searchWord, colIdx):
    time_start = time.time()
    df_in = pd.read_excel(fileIn)
    time_load = time.time()
    print("loaded excel file in {:,.1f} secs".format(time_load - time_start))

    print("{:<7} - {:15} - {:15} - {:30} - {:30} - {:15} - {:<15}".format("Emri", "Mbiemri", "EMRI I PLOTE", "Subjekti", "DRT", "Paga Bruto", "Profesioni"))
    df_out = pd.DataFrame()
    count = 0
    added = 0
    for r in df_in.itertuples(index=True, name='Pandas'):
        count = count + 1
        cellValue = r[colIdx]
        if searchWord.lower() in str(cellValue).lower():
            try:
                # print("{:<7} - {:15} - {:15} - {:30} - {:30} - {:15} - {:,.2f}".format(r[0], r[1].ljust(15)[:15], r[2], r[3], r[4].ljust(30)[:30], r[5], int(r[6])))
                # row = pd.Series([r[0], r[1], r[2], r[3], r[4], r[5], "{:,.2f}".format(r[6]), r[7]])
                row = pd.Series([r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]])
            except:
                print("Exception for: {:<7} - {:15} - {:15} - {:30} - {:30} - {:15} - {:15}".format(r[0], r[1].ljust(15)[:15], r[2], r[3], r[4].ljust(30)[:30], r[5], r[6]))
                row = pd.Series([r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]])
            row_df = pd.DataFrame([row])
            df_out = pd.concat([row_df, df_out])
            added = added + 1

    time_scan = time.time()
    print("scanned dataframe with {} rows in {:,.1f} secs. Added {} rows".format(count, time_scan - time_load, added))

    writer = pd.ExcelWriter(fileOut, engine='xlsxwriter')
    df_out.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    time_write = time.time()
    print("wrote output in {:,.1f} secs in file ".format(time_write - time_scan, fileOut))


if __name__ == "__main__":
    searchWord = "name surname"
    columnIndex = 4

    fileIn = "janar_1cent.xlsx"
    fileOut = "search_" + searchWord + "_" + str(columnIndex) + ".xlsx"
    searchInExcel(fileIn, fileOut, searchWord, columnIndex)
    print("Search for {}".format(searchWord))
