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

selected_columns = ['명칭']

region_mapping = {
    '강남구': 1, '강동구': 2, '강북구': 3, '강서구': 4, '관악구': 5,
    '광진구': 6, '구로구': 7, '금천구': 8, '노원구': 9, '도봉구': 10,
    '동대문구': 11, '동작구': 12, '마포구': 13, '서대문구': 14, '서초구': 15,
    '성동구': 16, '성북구': 17, '송파구': 18, '양천구': 19, '영등포구': 20,
    '용산구': 21, '은평구': 22, '종로구': 23, '중구': 24, '중랑구': 25
}
df['region_id'] = df['행정 구'].map(region_mapping)
df.loc[df['행정 구'].isna(), 'region_id'] = 26
print(df['region_id'])

df['facility_type'] = 'PARK'

df_selected = df[selected_columns + ['facility_type'] + ['region_id']]
df_selected = df_selected.fillna('')

query = f"INSERT INTO facility (name, facility_type, region_id) VALUES (%s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
