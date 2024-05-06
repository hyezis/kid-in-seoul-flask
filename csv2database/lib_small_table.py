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

df = pd.read_csv('./csv/lib_small.csv', encoding='utf-8')

selected_columns = ['홈페이지 URL', '위도', '경도', '운영시간', '전화번호', '주소', '구명']

# 686~1807
df['facility_id'] = range(686, 1808)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO library (homepage_url, latitude, longitude, operating_time, phone_num, post_num, region_gu, facility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
