import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="편의점 & 카페 지도", page_icon="📍", layout="wide")

st.title("📍 편의점 및 카페 위치 지도")

# 2. 데이터 불러오기 (샘플 데이터)
@st.cache_data
def load_data():
    data = [
        {"name": "CU 제주공항점", "category": "편의점", "lat": 33.5066, "lon": 126.4928},
        {"name": "GS25 제주연동점", "category": "편의점", "lat": 33.4880, "lon": 126.4900},
        {"name": "세븐일레븐 노형점", "category": "편의점", "lat": 33.4840, "lon": 126.4800},
        {"name": "스타벅스 제주공항DT점", "category": "카페", "lat": 33.5000, "lon": 126.4800},
        {"name": "투썸플레이스 제주시청점", "category": "카페", "lat": 33.4990, "lon": 126.5300},
        {"name": "에이바우트커피 신제주점", "category": "카페", "lat": 33.4850, "lon": 126.4920},
        {"name": "빽다방 제주연동점", "category": "카페", "lat": 33.4890, "lon": 126.4910},
    ]
    return pd.DataFrame(data)

df = load_data()

# 3. 사이드바 - 카테고리 필터링
st.sidebar.header("🔍 검색 및 필터")
selected_categories = st.sidebar.multiselect(
    "표시할 매장 유형을 선택하세요:",
    options=["편의점", "카페"],
    default=["편의점", "카페"]
)

# 필터 적용 데이터
filtered_df = df[df["category"].isin(selected_categories)]

# 4. 상단 현황 카드 (전체, 편의점, 카페 수 표시)
total_count = len(filtered_df)
convenience_count = len(filtered_df[filtered_df["category"] == "편의점"])
cafe_count = len(filtered_df[filtered_df["category"] == "카페"])

col1, col2, col3 = st.columns(3)
col1.metric(label="🏪 전체 매장 수", value=f"{total_count}개")
col2.metric(label="🔵 편의점 수", value=f"{convenience_count}개")
col3.metric(label="🔴 카페 수", value=f"{cafe_count}개")

st.markdown("---")

# 5. 선명한 OpenStreetMap 지형 생성
# 한국어 지명과 주요 도로가 뚜렷하게 노출되는 기본 타일 사용
m = folium.Map(
    location=[33.4950, 126.4950],
    zoom_start=13,
    tiles="OpenStreetMap"
)

# 6. 또렷한 아이콘 마커 찍기
for _, row in filtered_df.iterrows():
    if row["category"] == "편의점":
        color = "blue"
        icon_name = "shopping-cart"
    else:
        color = "red"
        icon_name = "coffee"

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(f"<b>{row['name']}</b><br>유형: {row['category']}", max_width=200),
        tooltip=f"{row['name']} ({row['category']})",
        icon=folium.Icon(color=color, icon=icon_name, prefix="fa")
    ).add_to(m)

# 7. 지도 화면 출력
st_folium(m, width="100%", height=520, returned_objects=[])
