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

df = pd.read_csv('./csv/kids_cafe.csv', encoding='utf-8')

selected_columns = ['기본주소', '신청가능연령', '휴관일', 'x좌표값', 'y좌표값', '운영일', '연락처', '행정동명', '자치구명', '이용정원(개인)']

# 176~202
df['facility_id'] = range(176, 203)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO kids_cafe (address, available_age, closed_days, latitude, longitude, operating_days, phone_num, region_dong, region_gu, usage_capacity, facility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
