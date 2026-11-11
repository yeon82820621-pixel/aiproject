
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

# ==================================
# 1. 페이지 설정
# ==================================
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령별 인구 분석")
st.write("행정구역, 연도, 성별을 선택하여 연령별 인구를 확인하세요.")

# ==================================
# 2. CSV 파일 경로 설정
# app.py는 pages 폴더 안에 있고
# CSV는 상위 폴더에 있음
# ==================================
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "population.csv"

# ==================================
# 3. CSV 파일 불러오기
# ==================================
@st.cache_data
def load_data(file_path):
    encodings = ["cp949", "euc-kr", "utf-8-sig", "utf-8"]

    for encoding in encodings:
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding
            )
            return df
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 인코딩을 확인해주세요.")

if not CSV_PATH.exists():
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

try:
    df = load_data(CSV_PATH)
except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()

# ==================================
# 4. 행정구역 이름 정리
# ==================================
df["지역명"] = (
    df["행정구역"]
    .astype(str)
    .str.replace(r"\s*\(\d+\)\s*$", "", regex=True)
    .str.strip()
)

region_list = df["지역명"].tolist()

# ==================================
# 5. 선택 메뉴
# ==================================
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox(
        "📍 행정구역 선택",
        region_list
    )

with col2:
    selected_year = st.selectbox(
        "📅 연도 선택",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

with col3:
    selected_gender = st.selectbox(
        "👥 성별 선택",
        ["전체", "남자", "여자"]
    )

# ==================================
# 6. 선택한 데이터 추출
# ==================================
age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

gender_prefix = {
    "전체": "",
    "남자": "남_",
    "여자": "여_"
}

selected_data = df[
    df["지역명"] == selected_region
].iloc[0]

population = []

for age in age_groups:

    column_name = (
        f"{selected_year}년_"
        f"{gender_prefix[selected_gender]}"
        f"거주자_{age}"
    )

    if column_name not in df.columns:
        st.error(
            f"해당 데이터 열을 찾을 수 없습니다: {column_name}"
        )
        st.stop()

    value = pd.to_numeric(
        selected_data[column_name],
        errors="coerce"
    )

    population.append(
        0 if pd.isna(value) else int(value)
    )

# ==================================
# 7. 그래프 데이터 생성
# ==================================
chart_df = pd.DataFrame({
    "연령대": age_groups,
    "인구수": population
})

# ==================================
# 8. 총인구수 표시
# ==================================
st.subheader(
    f"{selected_region} {selected_year}년 "
    f"{selected_gender} 연령별 인구"
)

st.metric(
    "총인구수",
    f"{sum(population):,}명"
)

# ==================================
# 9. 꺾은선 그래프
# ==================================
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["연령대"],
        y=chart_df["인구수"],
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="green",
            width=3
        ),
        marker=dict(
            color="green",
            size=8
        ),
        hovertemplate=(
            "나이: %{x}<br>"
            "인구수: %{y:,}명"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title="연령대별 인구 분포",
    xaxis_title="나이",
    yaxis_title="인구수 (명)",
    height=600,
    template="plotly_white",
    hovermode="x unified",
    font=dict(
        family="Malgun Gothic, NanumGothic, sans-serif",
        size=13
    ),
    xaxis=dict(
        type="category",
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        rangemode="tozero",
        dtick=1000,
        tick0=0,
        tickformat=",",
        showgrid=True,
        gridcolor="lightgray",
        gridwidth=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# 10. 데이터 표
# ==================================
with st.expander("📋 연령별 인구 데이터 확인"):

    display_df = chart_df.copy()

    display_df["인구수"] = display_df[
        "인구수"
    ].map(lambda x: f"{x:,}명")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

st.caption("데이터 출처: population.csv")
