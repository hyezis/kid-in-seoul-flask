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

df = pd.read_csv('./csv2database/csv/art_gallery.csv', encoding='utf-8')

selected_columns = ['소재지도로명주소', '어른관람료', '어린이관람료', '관리기관전화번호', '운영홈페이지']

# 1~175
df['facility_id'] = range(1,176)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO art_gallery (address, adult_fee, child_fee, phone_num, url, facility_id) VALUES (%s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
