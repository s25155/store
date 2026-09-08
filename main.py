import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="편의점 & 카페 지도", page_icon="📍", layout="wide")
st.title("📍 편의점 및 카페 위치 지도 (Folium 버전)")

# 샘플 데이터
data = [
    {"name": "CU 제주공항점", "category": "편의점", "lat": 33.5066, "lon": 126.4928},
    {"name": "GS25 제주연동점", "category": "편의점", "lat": 33.4880, "lon": 126.4900},
    {"name": "스타벅스 제주공항DT점", "category": "카페", "lat": 33.5000, "lon": 126.4800},
    {"name": "투썸플레이스 제주시청점", "category": "카페", "lat": 33.4990, "lon": 126.5300},
]
df = pd.DataFrame(data)

# 필터
selected = st.multiselect("카테고리 선택", ["편의점", "카페"], default=["편의점", "카페"])
filtered_df = df[df["category"].isin(selected)]

# 기본 지도 생성 (OpenStreetMap 기반 - 밝은 일반 지도)
m = folium.Map(location=[33.4995, 126.5312], zoom_start=12)

# 마커(점) 추가
for _, row in filtered_df.iterrows():
    # 편의점은 파란색, 카페는 빨간색
    color = "blue" if row["category"] == "편의점" else "red"
    
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,
        popup=row["name"],
        tooltip=f"{row['name']} ({row['category']})",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=1000, height=500)
