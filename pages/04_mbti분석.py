
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

DATA_FILE = Path(__file__).parent / "countriesMBTI_16types.csv"

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    data["Country"] = data["Country"].astype(str).str.strip()
    mbti_columns = [c for c in data.columns if c != "Country"]

    for c in mbti_columns:
        data[c] = pd.to_numeric(data[c], errors="coerce")

    return data.dropna(subset=["Country"]), mbti_columns

try:
    df, mbti_types = load_data(DATA_FILE)
except FileNotFoundError:
    st.error("CSV 파일을 app.py와 같은 폴더에 넣어주세요.")
    st.stop()

countries = sorted(df["Country"].unique())
selected_country = st.selectbox("국가 선택", countries)

country_row = df[df["Country"] == selected_country].iloc[0]

chart_data = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [country_row[m] * 100 for m in mbti_types]
}).dropna().sort_values("비율", ascending=False).reset_index(drop=True)

blue_gradient = [
    "#1769D2", "#2878D8", "#3987DE", "#4A96E4",
    "#5BA5EA", "#6CB4F0", "#7DC3F6", "#8ED2FC",
    "#9DDCFF", "#ACE4FF", "#BBEAFF", "#CAF0FF",
    "#D5F3FF", "#DFF6FF", "#E8F9FF"
]

bar_colors = ["#E53935"] + blue_gradient[:len(chart_data)-1]

st.subheader(f"📊 {selected_country}의 MBTI 비율")

col1, col2 = st.columns(2)
col1.metric("가장 높은 MBTI", chart_data.iloc[0]["MBTI"])
col2.metric("1위 비율", f'{chart_data.iloc[0]["비율"]:.2f}%')

fig = px.bar(
    chart_data,
    x="MBTI",
    y="비율",
    text=chart_data["비율"].map(lambda x: f"{x:.2f}%"),
    title=f"{selected_country} - MBTI 유형별 비율"
)

fig.update_traces(
    marker_color=bar_colors,
    textposition="outside",
    cliponaxis=False,
    hovertemplate="%{x}<br>비율: %{y:.2f}%<extra></extra>"
)

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis=dict(rangemode="tozero"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.caption("빨간색은 1위, 파란색 계열은 나머지 MBTI 유형입니다.")

with st.expander("MBTI 비율 상세 표"):
    display_data = chart_data.copy()
    display_data["비율"] = display_data["비율"].map(lambda x: f"{x:.2f}%")
    st.dataframe(display_data, use_container_width=True)

with st.expander("전체 국가 데이터"):
    st.dataframe(df, use_container_width=True)

st.download_button(
    "📥 분석 결과 다운로드",
    data=chart_data.to_csv(index=False).encode("utf-8-sig"),
    file_name="MBTI_analysis.csv",
    mime="text/csv"
)
