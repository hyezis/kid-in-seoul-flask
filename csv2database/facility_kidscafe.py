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

selected_columns = ['시설명']

df['facility_type'] = 'KIDSCAFE'

df_selected = df[selected_columns + ['facility_type']]

df_selected = df_selected.fillna('')

query = f"INSERT INTO facility (facility_type, name) VALUES (%s, %s);"

for index, row in df_selected.iterrows():

    cursor.execute(query, tuple(row))

conn.commit()

cursor.close()
conn.close()

print("**DONE**")
