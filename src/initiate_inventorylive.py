import sqlite3
import pandas
import pprint
import time

inv_xlsx_file = r'../dat/inglist.xlsx'

inv_df = pandas.read_excel(inv_xlsx_file)

print(inv_df.shape)
print(inv_df.columns)

invlist = inv_df.values.tolist()[1:]

conn = sqlite3.connect(r'../dat/inventory_live_db.db')
print("\n")
itemid = 1
for item in invlist:
    # print(item)
    print("INSERTING ITEM:  ", itemid, item[0], item[1], "0", item[2])
    conn.cursor().execute("INSERT INTO inventory_live VALUES (NULL, ?, ?, ?, ?, ?)", (str(itemid), str(item[0]), str(item[1]), "0", str(item[2]), ))
    conn.commit()
    itemid += 1
    time.sleep(0.3)