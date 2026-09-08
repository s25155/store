import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="편의점 & 카페 지도", page_icon="📍", layout="wide")
st.title("📍 편의점 및 카페 위치 지도")

# 샘플 데이터 (제주도 기준 예시)
@st.cache_data
def load_data():
    data = [
        # 편의점 (파란색)
        {"name": "CU 제주공항점", "category": "편의점", "lat": 33.5066, "lon": 126.4928, "color": [0, 102, 255, 230]},
        {"name": "GS25 제주연동점", "category": "편의점", "lat": 33.4880, "lon": 126.4900, "color": [0, 102, 255, 230]},
        {"name": "세븐일레븐 서귀포점", "category": "편의점", "lat": 33.2500, "lon": 126.5600, "color": [0, 102, 255, 230]},
        
        # 카페 (빨간색)
        {"name": "스타벅스 제주공항DT점", "category": "카페", "lat": 33.5000, "lon": 126.4800, "color": [255, 51, 51, 230]},
        {"name": "투썸플레이스 제주시청점", "category": "카페", "lat": 33.4990, "lon": 126.5300, "color": [255, 51, 51, 230]},
        {"name": "에이바우트커피 신제주점", "category": "카페", "lat": 33.4850, "lon": 126.4920, "color": [255, 51, 51, 230]},
    ]
    return pd.DataFrame(data)

df = load_data()

# 사이드바 필터
st.sidebar.header("필터")
selected_categories = st.sidebar.multiselect(
    "표시할 장소:",
    options=["편의점", "카페"],
    default=["편의점", "카페"]
)

filtered_df = df[df["category"].isin(selected_categories)]

# 지도 레이어 생성
layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_df,
    get_position=["lon", "lat"],
    get_color="color",
    get_radius=150,  # 지도 확대에 맞춰 점 크기 조정
    radius_scale=1,
    radius_min_pixels=8,  # 최소 픽셀 크기 지정 (축소해도 점이 보임)
    radius_max_pixels=30,
    pickable=True,
)

# 중심 위치 설정
center_lat = filtered_df["lat"].mean() if not filtered_df.empty else 33.4995
center_lon = filtered_df["lon"].mean() if not filtered_df.empty else 126.5312

view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=11,
    pitch=0,
)

# 💡 map_style을 'light' 또는 'road'로 지정하여 밝은 기본 지도로 출력합니다.
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="road",  # 또는 "light"
    tooltip={"html": "<b>{name}</b><br/>유형: {category}"}
)

st.pydeck_chart(r)
