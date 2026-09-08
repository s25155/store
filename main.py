import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="편의점 & 카페 지도 앱",
    page_icon="📍",
    layout="wide"
)

st.title("📍 편의점 및 카페 위치 지도")
st.markdown("지도 위에서 편의점(파란색)과 카페(빨간색)의 위치를 확인하세요.")

# 2. 샘플 데이터 생성 (서울 주요 지역 좌표 예시)
# 실제 데이터가 있다면 CSV 파일 등을 pd.read_csv()로 불러와 사용하시면 됩니다.
@st.cache_data
def load_data():
    data = [
        # 편의점 데이터 (카테고리: convenience, 색상: 파란색 [RGB, Alpha])
        {"name": "GS25 강남점", "category": "편의점", "lat": 37.4979, "lon": 127.0276, "color": [0, 122, 255, 200]},
        {"name": "CU 역삼점", "category": "편의점", "lat": 37.5006, "lon": 127.0364, "color": [0, 122, 255, 200]},
        {"name": "세븐일레븐 선릉점", "category": "편의점", "lat": 37.5045, "lon": 127.0490, "color": [0, 122, 255, 200]},
        {"name": "이마트24 홍대점", "category": "편의점", "lat": 37.5563, "lon": 126.9226, "color": [0, 122, 255, 200]},
        
        # 카페 데이터 (카테고리: cafe, 색상: 빨간색 [RGB, Alpha])
        {"name": "스타벅스 강남역점", "category": "카페", "lat": 37.4985, "lon": 127.0280, "color": [255, 59, 48, 200]},
        {"name": "투썸플레이스 역삼점", "category": "카페", "lat": 37.5012, "lon": 127.0355, "color": [255, 59, 48, 200]},
        {"name": "빽다방 선릉역점", "category": "카페", "lat": 37.5038, "lon": 127.0482, "color": [255, 59, 48, 200]},
        {"name": "할리스 홍대점", "category": "카페", "lat": 37.5550, "lon": 126.9235, "color": [255, 59, 48, 200]},
    ]
    return pd.DataFrame(data)

df = load_data()

# 3. 사이드바 필터 옵션
st.sidebar.header("필터 옵션")
selected_categories = st.sidebar.multiselect(
    "표시할 장소 유형을 선택하세요:",
    options=["편의점", "카페"],
    default=["편의점", "카페"]
)

# 필터링된 데이터
filtered_df = df[df["category"].isin(selected_categories)]

# 4. 지도 레이어 설정 (pydeck 사용)
layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_df,
    get_position=["lon", "lat"],
    get_color="color",
    get_radius=50,  # 점의 반지름 (미터 단위)
    pickable=True,  # 마우스 호버(Hover) 시 정보 표시 여부
    auto_highlight=True,
)

# 기본 중심 좌표 (데이터의 평균 위치)
if not filtered_df.empty:
    center_lat = filtered_df["lat"].mean()
    center_lon = filtered_df["lon"].mean()
else:
    center_lat, center_lon = 37.5665, 126.9780  # 데이터가 없을 경우 서울시청 기준

view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=13,
    pitch=0,
)

# 툴팁 (마우스를 올렸을 때 나오는 정보)
tooltip = {
    "html": "<b>{name}</b><br/>유형: {category}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# 5. 지도 출력
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

st.pydeck_chart(r)

# 범례(Legend) 및 데이터 테이블 표시
st.markdown("""
<div style="display: flex; gap: 20px; margin-bottom: 10px;">
    <div>🔵 <b>편의점</b></div>
    <div>🔴 <b>카페</b></div>
</div>
""", unsafe_allow_html=True)

with st.expander("원본 데이터 보기"):
    st.dataframe(filtered_df[["name", "category", "lat", "lon"]])
