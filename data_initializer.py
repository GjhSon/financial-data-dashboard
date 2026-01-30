import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# 연결엔진
user = "root"
password = ""
safe_password = urllib.parse.quote_plus(password)
host = "localhost"
port = "3306"
db_name = "yongin_card_usage"


engine = create_engine(f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{db_name}")


df = pd.read_csv('C:/data/yongin_card_usage.csv', nrows = 10000)
df = df.rename(columns = {'sex' : 'gender'})
df = df.rename(columns = {'day' : '_day'})
df['ta_ymd'] = pd.to_datetime(df['ta_ymd'], format = '%Y%m%d')
df.to_sql(name = 'yongin_card_usage_11', con = engine, if_exists = 'append', index = False)
print("Success!")

