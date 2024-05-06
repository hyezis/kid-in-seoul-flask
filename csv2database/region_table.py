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

region_gu = ['강남구', '강동구', '강북구', '강서구', '관악구', 
             '광진구', '구로구', '금천구', '노원구', '도봉구', 
             '동대문구', '동작구', '마포구', '서대문구', '서초구', 
             '성동구', '성북구', '송파구', '양천구', '영등포구', 
             '용산구', '은평구', '종로구', '중구', '중랑구']

query = f"INSERT INTO region (region_name) VALUES (%s);"

for gu in region_gu:
    cursor.execute(query, (gu,))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
