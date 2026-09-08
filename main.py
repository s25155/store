import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="편의점 & 카페 위치 지도", page_icon="📍", layout="wide")

st.title("📍 편의점 및 카페 위치 지도")

# 2. 데이터 불러오기 (샘플 데이터)
@st.cache_data
def load_data():
    data = [
        {"name": "CU 제주공항점", "category": "편의점", "lat": 33.5066, "lon": 126.4928},
        {"name": "GS25 제주연동점", "category": "편의점", "lat": 33.4880, "lon": 126.4900},
        {"name": "세븐일레븐 노형점", "category": "편의점", "lat": 33.4840, "lon": 126.4800},
        {"name": "CU 용담점", "category": "편의점", "lat": 33.5120, "lon": 126.5100},
        {"name": "GS25 제주시청점", "category": "편의점", "lat": 33.4990, "lon": 126.5310},
        {"name": "스타벅스 제주공항DT점", "category": "카페", "lat": 33.5000, "lon": 126.4800},
        {"name": "투썸플레이스 제주시청점", "category": "카페", "lat": 33.4990, "lon": 126.5300},
        {"name": "에이바우트커피 신제주점", "category": "카페", "lat": 33.4850, "lon": 126.4920},
        {"name": "빽다방 제주연동점", "category": "카페", "lat": 33.4890, "lon": 126.4910},
        {"name": "컴포즈커피 노형점", "category": "카페", "lat": 33.4830, "lon": 126.4750},
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

# 4. 상단 현황 수치 카드 스타일링 (CSS)
st.markdown("""
<style>
.card-container {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
}
.metric-card {
    flex: 1;
    padding: 15px 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.card-total { background-color: #00A896; }
.card-convenience { background-color: #0088FF; }
.card-cafe { background-color: #D81B60; }

.card-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
}
.card-value {
    font-size: 32px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# 5. 상단 현황 카드 개수 계산 및 표시
total_count = len(filtered_df)
convenience_count = len(filtered_df[filtered_df["category"] == "편의점"])
cafe_count = len(filtered_df[filtered_df["category"] == "카페"])

st.markdown(f"""
<div class="card-container">
    <div class="metric-card card-total">
        <div class="card-title">🏪 전체 매장 수</div>
        <div class="card-value">{total_count}개</div>
    </div>
    <div class="metric-card card-convenience">
        <div class="card-title">🔵 편의점 수</div>
        <div class="card-value">{convenience_count}개</div>
    </div>
    <div class="metric-card card-cafe">
        <div class="card-title">🔴 카페 수</div>
        <div class="card-value">{cafe_count}개</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. 지도 생성 (CartoDB Positron - 연한 배경으로 점이 가장 또렷해 보이는 스타일)
if not filtered_df.empty:
    center_lat = filtered_df["lat"].mean()
    center_lon = filtered_df["lon"].mean()
else:
    center_lat, center_lon = 33.4950, 126.4950

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="CartoDB positron"
)

# 7. 흰색 테두리가 있는 선명하고 또렷한 원형 점 마커 추가
for _, row in filtered_df.iterrows():
    # 이미지와 동일한 또렷한 컬러 선별
    color = "#0088FF" if row["category"] == "편의점" else "#D81B60"
    
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,                       # 점 크기
        color="#FFFFFF",                # 흰색 테두리로 또렷함 극대화
        weight=2.5,                     # 테두리 두께
        fill=True,
        fill_color=color,               # 내부 색상
        fill_opacity=0.9,               # 선명한 투명도
        popup=folium.Popup(f"<b>{row['name']}</b><br>유형: {row['category']}", max_width=200),
        tooltip=f"{row['name']} ({row['category']})"
    ).add_to(m)

# 8. 지도 화면 출력
st_folium(m, width=None, height=520)
