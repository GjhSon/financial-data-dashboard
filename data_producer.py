import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import time 


# 연결엔진
user = "root"
password = ""
safe_password = urllib.parse.quote_plus(password)
host = "localhost"
port = "3306"
db_name = "yongin_card_usage"


engine = create_engine(f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{db_name}")

query = "select count(*) as cnt from yongin_card_usage_11"


current_count_df = pd.read_sql(query, engine)
current_count = current_count_df['cnt'][0]

df_remain = pd.read_csv("C:/data/yongin_card_usage.csv").iloc[current_count : ]
df_remain = df_remain.rename(columns = {'sex' : 'gender'})
df_remain = df_remain.rename(columns = {'day' : '_day'})
df_remain['ta_ymd'] = pd.to_datetime(df_remain['ta_ymd'], format = '%Y%m%d')
print("실시간 데이터 유입 환경 시뮬레이션 시작...")

batch_size = 5
for i in range(0 , len(df_remain), batch_size):
    batch = df_remain.iloc[i : i + batch_size]
    batch.to_sql(name = 'yongin_card_usage_11', con = engine, if_exists = 'append', index = False)
    print(f"{current_count + i + len(batch)}번째 데이터까지 적재 완료")
    time.sleep(0.2)

