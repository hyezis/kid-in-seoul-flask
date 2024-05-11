import pandas as pd
import pymysql
import config
import re

# DB Connection
conn = pymysql.connect(
    host=config.DB_CONFIG['host'], 
    port=3306, 
    user=config.DB_CONFIG['user'], 
    passwd=config.DB_CONFIG['passwd'], 
    db=config.DB_CONFIG['db'], 
    charset='utf8'
)
cursor = conn.cursor()

df = pd.read_csv('./csv2database/csv/event.csv', encoding='utf-8')

selected_columns = ['축제명']

df['facility_type'] = 'EVENT'
df['region_id'] = 26

df_selected = df[selected_columns + ['facility_type'] + ['region_id']]
df_selected = df_selected.fillna('')

query = f"INSERT INTO facility (name, facility_type, region_id) VALUES (%s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
