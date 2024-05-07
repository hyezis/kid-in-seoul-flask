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

df = pd.read_csv('./csv2database/csv/outdoor.csv', encoding='utf-8')

selected_columns = ['기본주소', '연령구분', '상세주소', '사용료', '사용료무료여부', 'X좌표값', 'Y좌표값', '우편번호', '자치구명', '안내URL']

# 1356~3814
df['facility_id'] = range(1356, 3815)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO outdoor_facility (address, age_classification, detail_address, fee, free, latitude, longitude, post_num, region_gu, url_link, facility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
