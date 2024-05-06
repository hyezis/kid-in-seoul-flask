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

df = pd.read_csv('./csv/kinder.csv', encoding='utf-8')

selected_columns = ['상세주소', '팩스번호', '제공서비스', '어린이집명', '전화번호', '우편번호', '시군구명', '어린이집유형']

region_mapping = {
    '강남구': 1, '강동구': 2, '강북구': 3, '강서구': 4, '관악구': 5,
    '광진구': 6, '구로구': 7, '금천구': 8, '노원구': 9, '도봉구': 10,
    '동대문구': 11, '동작구': 12, '마포구': 13, '서대문구': 14, '서초구': 15,
    '성동구': 16, '성북구': 17, '송파구': 18, '양천구': 19, '영등포구': 20,
    '용산구': 21, '은평구': 22, '종로구': 23, '중구': 24, '중랑구': 25
}

df['region_id'] = df['시군구명'].map(region_mapping)

df_selected = df[selected_columns + ['region_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO kindergarden (address, fax_num, feature, kg_name, phone_num, post_num, region_gu, type, region_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
