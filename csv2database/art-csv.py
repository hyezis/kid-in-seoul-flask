import pandas as pd
import pymysql
import config
import re

def extract_gu(address):
    if pd.isna(address):
        return None
    gu_pattern = re.compile(r'\w+구') # '구'로 끝나는 단어 추출
    match = gu_pattern.search(address)
    if match:
        return match.group()
    else:
        return None

df = pd.read_csv('./csv2database/csv/art_gallery.csv', encoding='utf-8')

# '자치구명' 열을 추가하여 '소재지도로명주소'에서 자치구를 추출하여 넣습니다.
df['자치구명'] = df['소재지도로명주소'].apply(extract_gu)

df = df[['시설명','박물관미술관구분','소재지도로명주소','소재지지번주소','위도','경도',
         '운영기관전화번호','운영기관명','운영홈페이지','편의시설정보','평일관람시작시각',
         '평일관람종료시각','공휴일관람시작시각','공휴일관람종료시각','휴관정보','어른관람료',
         '청소년관람료','어린이관람료','관람료기타정보','박물관미술관소개','교통안내정보',
         '관리기관전화번호','관리기관명','데이터기준일자','자치구명']]

# CSV 파일로 저장
df.to_csv('./csv2database/csv/art_gallery_gu.csv', index=False, encoding='utf-8')

print("**DONE**")
