import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from streamlit_autorefresh import st_autorefresh

# 자동 새로고침 (5초마다)
count = st_autorefresh(interval = 5000, key = "datarefresh")

# 연결엔진
user = "root"
password = ""
safe_password = urllib.parse.quote_plus(password)
host = "localhost"
port = "3306"
db_name = "yongin_card_usage"


engine = create_engine(f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{db_name}")


# 데이터 전처리
hour_mapping = {
        "00:00 ~ 06:59": 1,
        "07:00 ~ 08:59": 2,
        "09:00 ~ 10:59": 3,
        "11:00 ~ 12:59": 4,
        "13:00 ~ 14:59": 5,
        "15:00 ~ 16:59": 6,
        "17:00 ~ 18:59": 7,
        "19:00 ~ 20:59": 8,
        "21:00 ~ 22:59": 9,
        "23:00 ~ 23:59": 10
    }

age_mapping = {
        "10~19세" : 2,
        "20~29세" : 3, 
        "30~39세" : 4, 
        "40~49세" : 5, 
        "50~59세" : 6, 
        "60~69세" : 7, 
        "70~79세" : 8, 
        "80~89세" : 9, 
        "90~99세" : 10
    }

day_mapping = {
        "월요일" : 1,
        "화요일" : 2,
        "수요일" : 3,
        "목요일" : 4,
        "금요일" : 5,
        "토요일" : 6,
        "일요일" : 7
    }


# 대시보드 제목 및 설명
st.title("💳 경기도 용인시 카드 소비 현황")
st.markdown("-> 상세 조건 설정을 통해 용인시 카드 소비 현황을 실시간으로 확인해보세요.")
st.markdown("-> 확인하고자 하는 소비 카테고리, 시간대, 연령대, 성별, 요일을 좌측 필터를 통해 선택해주세요.")

# 좌측 필터 설정 : 소비 카테고리, 시간대, 연령대, 성별, 요일
st.sidebar.header("아래의 필터를 선택해주세요.")

category_option = st.sidebar.selectbox(
    "소비 카테고리를 선택해주세요.",
    ("전체", "가전제품", "건강/기호식품", "사무/교육용품", "서적/도서", "선물/완구", "스포츠/레져용품", "음/식료품소매", "의복/의류", "인테리어/가정용품",
     "종합소매점", "차량관리/부품", "차량", "악기/공예", "패션잡화", "화장품소매", "기타용품", "제조/도매", "광고/인쇄/인화", "미용서비스", "전문서비스",
     "사우나/휴게시설", "세탁/가사서비스", "연료", "차량관리/서비스", "보안/운송", "무점포서비스", "금융상품/서비스", "숙박", "일반스포츠", "취미/오락",
     "간이주점", "고기요리", "닭/오리요리", "별식/퓨전요리", "뷔페", "분식", "양식", "유흥주점", "일식/수산물", "제과/제빵/떡/케익", "중식", "커피/음료",
     "패스트푸드", "한식", "휴게소/대형업체", "독서실/고시원", "기타교육", "예체능계학원", "외국어학원", "유아교육", "입시학원", "자동차학원", "수의업", 
     "의약/의료품", "일반병원", "특화병원", "공연관람", "문화서비스", "인터넷쇼핑", "기업", "가례서비스", "회비/공과금", "기타의료", "전시장", "기타결제",
     "단체", "수리서비스", "음식배달서비스", "경기관람", "렌탈서비스", "공공기관")
)

hour_option = st.sidebar.selectbox(
    "시간대를 선택해주세요.",
    ("전체", "00:00 ~ 06:59", "07:00 ~ 08:59", "09:00 ~ 10:59", "11:00 ~ 12:59", "13:00 ~ 14:59", "15:00 ~ 16:59", "17:00 ~ 18:59", "19:00 ~ 20:59",
     "21:00 ~ 22:59", "23:00 ~ 23:59")
)

age_option = st.sidebar.selectbox(
    "연령대를 선택해주세요.",
    ("전체", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세")
)

gender_option = st.sidebar.selectbox(
    "성별을 선택해주세요.",
    ("전체", "M", "F")
)

day_option = st.sidebar.selectbox(
    "요일을 선택해주세요.",
    ("전체", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일")
)


# SQL 쿼리 작성 (사용자 선택에 따라 동적으로 변함)
query = "select sum(amt) as total_amt, sum(cnt) as total_cnt from yongin_card_usage_11 where 1 = 1"

if category_option != "전체"  :
    query += f" and card_tpbuz_nm_2 = '{category_option}'"
if hour_option != "전체" :
    hour_number = hour_mapping[hour_option]
    query += f" and hour = '{hour_number}'"
if gender_option != "전체":
    query += f" and gender = '{gender_option}'"
if age_option != "전체" :
    age_number = age_mapping[age_option]
    query += f" and  age = '{age_number}'"
if day_option != "전체" :
    day_number = day_mapping[day_option]
    query += f" and _day = '{day_number}'"


# DB에서 데이터 가져오기
try:
    df_result = pd.read_sql(query, engine)
    total_usage = df_result['total_amt'][0]
    total_count = df_result['total_cnt'][0]

    
    if total_usage is None:
        total_usage = 0

    # 결과 화면 출력 
    st.subheader("📍 선택하신 필터를 통한 분석 결과")
    
    
    st.metric(label = "총 소비 금액", value = f"{total_usage :,.0f} 원")
    st.metric(label = "총 결제 횟수", value = f"{total_count :,.0f} 번")

except Exception as e:
    st.error(f"해당 조건에 맞는 소비 내역이 없습니다: {e}")

