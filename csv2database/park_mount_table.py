import pandas as pd
import pymysql
import config

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

df = pd.read_csv('./csv2database/csv/park_mount.csv', encoding='utf-8')

selected_columns = ['주소', '대표전화', '대분류', '행정 동', '행정 구', '행정 시']

# 203~347
df['facility_id'] = range(203, 348)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO park (address, call_number, main_category, region_dong, region_gu, region_si, facility_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
