
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.write("국가를 선택하면 해당 국가의 16가지 MBTI 유형별 비율을 확인할 수 있습니다.")

# 상위 폴더의 CSV 파일 경로
DATA_FILE = Path(__file__).parent.parent / "countriesMBTI_16types.csv"

# 데이터 불러오기
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)

    data["Country"] = data["Country"].astype(str).str.strip()

    mbti_columns = [
        column for column in data.columns
        if column != "Country"
    ]

    for column in mbti_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(subset=["Country"])

    return data, mbti_columns


try:
    df, mbti_types = load_data(DATA_FILE)

except FileNotFoundError:
    st.error(
        "CSV 파일을 찾을 수 없습니다. "
        "상위 폴더에 countriesMBTI_16types.csv가 있는지 확인해주세요."
    )
    st.stop()


# 국가 선택
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "🌎 분석할 국가를 선택하세요.",
    countries
)


# 선택 국가 데이터
country_row = df[
    df["Country"] == selected_country
].iloc[0]


# MBTI 비율 계산 및 정렬
chart_data = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [
        country_row[mbti] * 100
        for mbti in mbti_types
    ]
})

chart_data = (
    chart_data
    .dropna()
    .sort_values("비율", ascending=False)
    .reset_index(drop=True)
)


# 색상 설정
# 1위는 빨간색, 나머지는 파란색 그라데이션
blue_gradient = [
    "#1769D2",
    "#2878D8",
    "#3987DE",
    "#4A96E4",
    "#5BA5EA",
    "#6CB4F0",
    "#7DC3F6",
    "#8ED2FC",
    "#9DDCFF",
    "#ACE4FF",
    "#BBEAFF",
    "#CAF0FF",
    "#D5F3FF",
    "#DFF6FF",
    "#E8F9FF"
]

bar_colors = (
    ["#E53935"]
    + blue_gradient[:len(chart_data) - 1]
)


# 최고 비율 표시
st.subheader(
    f"📊 {selected_country}의 MBTI 비율"
)

col1, col2 = st.columns(2)

col1.metric(
    "가장 높은 MBTI 유형",
    chart_data.iloc[0]["MBTI"]
)

col2.metric(
    "1위 비율",
    f'{chart_data.iloc[0]["비율"]:.2f}%'
)


# 그래프 생성
fig = px.bar(
    chart_data,
    x="MBTI",
    y="비율",
    text=chart_data["비율"].map(
        lambda x: f"{x:.2f}%"
    ),
    title=f"{selected_country} - 16가지 MBTI 유형별 비율"
)


# 그래프 색상 및 디자인
fig.update_traces(
    marker_color=bar_colors,
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "%{x}<br>"
        "비율: %{y:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis=dict(
        rangemode="tozero"
    ),
    showlegend=False,
    margin=dict(
        t=70,
        b=30,
        l=20,
        r=20
    )
)


# 화면에 그래프 표시
st.plotly_chart(
    fig,
    use_container_width=True
)


st.caption(
    "🔴 빨간색: 해당 국가에서 비율이 가장 높은 MBTI 유형"
)

st.caption(
    "🔵 파란색: 나머지 MBTI 유형"
)


# 상세 데이터 표
with st.expander("📋 MBTI 비율 상세 표 보기"):

    display_data = chart_data.copy()

    display_data["비율"] = display_data[
        "비율"
    ].map(lambda x: f"{x:.2f}%")

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# 전체 국가 데이터
with st.expander("🌍 전체 국가 데이터 보기"):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# CSV 다운로드
st.download_button(
    label="📥 분석 결과 다운로드",

    data=chart_data.to_csv(
        index=False
    ).encode("utf-8-sig"),

    file_name="MBTI_analysis.csv",

    mime="text/csv"
)


st.divider()

st.caption(
    "Countries MBTI 16 Types Data Analysis"
)
