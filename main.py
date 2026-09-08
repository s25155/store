import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="편의점 & 카페 지도",
    page_icon="📍",
    layout="wide"
)

st.title("📍 편의점 및 카페 위치 지도")

# 2. 샘플 데이터 불러오기
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

# 3. 사이드바 - 카테고리 필터
st.sidebar.header("🔍 검색 및 필터")
selected_categories = st.sidebar.multiselect(
    "표시할 매장 유형을 선택하세요:",
    options=["편의점", "카페"],
    default=["편의점", "카페"]
)

# 필터링된 데이터
filtered_df = df[df["category"].isin(selected_categories)]

# 4. 상단 개수 표시 (st.metric)
total_count = len(filtered_df)
convenience_count = len(filtered_df[filtered_df["category"] == "편의점"])
cafe_count = len(filtered_df[filtered_df["category"] == "카페"])

col1, col2, col3 = st.columns(3)
col1.metric(label="🏪 전체 매장 수", value=f"{total_count}개")
col2.metric(label="🔵 편의점 수", value=f"{convenience_count}개")
col3.metric(label="🔴 카페 수", value=f"{cafe_count}개")

st.markdown("---")

# 5. 지도 생성 (OpenStreetMap - 한글 도로/지명 또렷한 기본 스타일)
# 데이터가 있을 경우 평균 위치로 이동
if not filtered_df.empty:
    center_lat = filtered_df["lat"].mean()
    center_lon = filtered_df["lon"].mean()
else:
    center_lat, center_lon = 33.4950, 126.4950

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="OpenStreetMap"
)

# 6. 표준 Glyphicon 아이콘 적용 (오류 방지 및 또렷한 핀)
for _, row in filtered_df.iterrows():
    if row["category"] == "편의점":
        color = "blue"
        icon_name = "shopping-cart"
    else:
        color = "red"
        icon_name = "glass"  # 카페/음료 표준 아이콘

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(f"<b>{row['name']}</b><br>유형: {row['category']}", max_width=200),
        tooltip=f"{row['name']} ({row['category']})",
        icon=folium.Icon(color=color, icon=icon_name)
    ).add_to(m)

# 7. 지도 화면 출력
st_folium(m, use_container_width=True, height=520, key="map")
