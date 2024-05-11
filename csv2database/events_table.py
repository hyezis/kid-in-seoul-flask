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

df = pd.read_csv('./csv2database/csv/event.csv', encoding='utf-8')

selected_columns = ['축제내용', '축제종료일자', '축제명', '개최장소', '축제시작일자']

# 4315~5987
df['facility_id'] = range(4315, 5988)

df_selected = df[selected_columns + ['facility_id']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO events (content, end_date, event_name, place, start_date, event_id) VALUES (%s, %s, %s, %s, %s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
