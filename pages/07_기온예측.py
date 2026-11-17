
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path
import re

# --------------------------------
# 페이지 설정
# --------------------------------

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 분석 및 예측")
st.write("과거 기온 데이터를 이용하여 미래의 평균기온을 예측합니다.")

# --------------------------------
# CSV 파일 불러오기
# --------------------------------

base_dir = Path(__file__).resolve().parent

# pages 폴더 안에 파이썬 파일이 있어도
# 상위 폴더에서 CSV 파일을 찾도록 설정
file_candidates = [
    base_dir / "temperature.csv",
    base_dir.parent / "temperature.csv"
]

file_path = next(
    (p for p in file_candidates if p.exists()),
    None
)

if file_path is None:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.stop()

# 한글 CSV 인코딩 처리
try:
    df = pd.read_csv(file_path, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding="utf-8-sig")

# --------------------------------
# 날짜 데이터 처리
# --------------------------------

required_columns = ["일시", "평균기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일에 필요한 열이 없습니다.")
    st.stop()

# 파일에 기록된 순서를 유지하면서
# 두 자리 연도의 세기를 순차적으로 복원
parsed_dates = []
previous_year = None

month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

for value in df["일시"]:

    match = re.match(
        r"([A-Za-z]{3})-(\d{2})",
        str(value).strip()
    )

    if not match:
        parsed_dates.append(pd.NaT)
        continue

    month_name = match.group(1).title()
    short_year = int(match.group(2))

    if month_name not in month_map:
        parsed_dates.append(pd.NaT)
        continue

    year = 1900 + short_year

    if previous_year is not None:
        while year < previous_year:
            year += 100

    previous_year = year

    parsed_dates.append(
        pd.Timestamp(
            year=year,
            month=month_map[month_name],
            day=1
        )
    )

df["날짜"] = parsed_dates

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

df = df.dropna(
    subset=["날짜", "평균기온(℃)"]
)

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# 날짜가 같은 데이터가 있으면 평균 처리
df = (
    df.groupby(["연도", "월"], as_index=False)
    ["평균기온(℃)"].mean()
)

df = df.sort_values(["연도", "월"])

# --------------------------------
# 사용자 입력
# --------------------------------

st.sidebar.header("🔍 분석 조건")

month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

selected_month = st.sidebar.selectbox(
    "분석할 월을 선택하세요",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x]
)

selected_year = st.sidebar.number_input(
    "예측할 연도를 입력하세요",
    min_value=int(df["연도"].min()),
    max_value=2100,
    value=int(df["연도"].max()) + 1,
    step=1
)

# --------------------------------
# 선택한 월 데이터 추출
# --------------------------------

month_df = df[
    df["월"] == selected_month
].copy()

if len(month_df) < 2:
    st.error("예측에 필요한 데이터가 부족합니다.")
    st.stop()

X = month_df[["연도"]]
y = month_df["평균기온(℃)"]

# --------------------------------
# 선형회귀 모델 학습
# --------------------------------

model = LinearRegression()

model.fit(X, y)

# 예측 기온 계산
prediction = model.predict(
    pd.DataFrame({"연도": [selected_year]})
)[0]

# 기존 데이터 예측값
month_df["회귀 예측기온"] = model.predict(X)

# 기울기와 절편
slope = model.coef_[0]
intercept = model.intercept_

# --------------------------------
# 예측 결과 표시
# --------------------------------

st.subheader(
    f"📊 {month_names[selected_month]} 평균기온 분석"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{selected_year}년"
    )

with col2:
    st.metric(
        "예측 평균기온",
        f"{prediction:.2f} ℃"
    )

with col3:
    st.metric(
        "기울기",
        f"{slope:.4f}"
    )

if selected_year > int(df["연도"].max()):
    st.warning(
        "과거 데이터 범위를 벗어난 미래 예측입니다. "
        "예측값은 실제 기온과 다를 수 있습니다."
    )

# --------------------------------
# 첫 번째 그래프
# 실제 기온 + 회귀 직선 + 미래 예측
# --------------------------------

st.subheader("1. 실제 기온과 선형회귀 예측 그래프")

min_year = int(month_df["연도"].min())
max_year = max(
    int(month_df["연도"].max()),
    int(selected_year)
)

graph_years = np.arange(
    min_year,
    max_year + 1
)

graph_predictions = model.predict(
    pd.DataFrame({"연도": graph_years})
)

fig = go.Figure()

# 실제 평균기온
fig.add_trace(
    go.Scatter(
        x=month_df["연도"],
        y=month_df["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="royalblue",
            size=7
        )
    )
)

# 선형회귀 직선
fig.add_trace(
    go.Scatter(
        x=graph_years,
        y=graph_predictions,
        mode="lines",
        name="선형회귀 예측선",
        line=dict(
            color="red",
            width=3
        )
    )
)

# 미래 예측 지점
fig.add_trace(
    go.Scatter(
        x=[selected_year],
        y=[prediction],
        mode="markers+text",
        name="미래 예측기온",
        text=[f"{prediction:.2f}℃"],
        textposition="top center",
        marker=dict(
            color="orange",
            size=14,
            symbol="star"
        )
    )
)

# 실제값과 회귀선 사이의 오차 표시
for _, row in month_df.iterrows():

    fig.add_shape(
        type="line",
        x0=row["연도"],
        x1=row["연도"],
        y0=row["평균기온(℃)"],
        y1=row["회귀 예측기온"],
        line=dict(
            color="gray",
            width=1,
            dash="dot"
        )
    )

fig.update_layout(
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="x unified",
    height=550,
    legend=dict(
        orientation="h",
        y=1.12
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 두 번째 그래프
# 오차 시각화
# --------------------------------

st.subheader("2. 선형회귀 예측 오차 그래프")

residuals = (
    month_df["평균기온(℃)"]
    - month_df["회귀 예측기온"]
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=month_df["연도"],
        y=residuals,
        mode="markers",
        name="실제값과 예측값의 차이",
        marker=dict(
            color="purple",
            size=7
        )
    )
)

fig2.add_hline(
    y=0,
    line_dash="dash",
    line_color="red",
    annotation_text="오차 0"
)

fig2.update_layout(
    xaxis_title="연도",
    yaxis_title="오차 (℃)",
    height=350
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------
# 선형회귀 알고리즘 설명
# --------------------------------

st.subheader("📖 선형회귀 알고리즘 쉽게 이해하기")

st.write("""
선형회귀는 과거에 수집한 데이터를 바탕으로
미래의 값을 예측하는 알고리즘입니다.

이 프로그램에서는 과거의 연도와 평균기온을 이용하여
두 값 사이의 관계를 직선으로 나타냅니다.
""")

st.latex(
    r"y = ax + b"
)

st.write("""
- x : 연도
- y : 평균기온
- a : 직선의 기울기
- b : 직선이 시작하는 위치를 결정하는 값

컴퓨터는 실제 기온 데이터와 직선 사이의 차이가
전체적으로 가장 작아지도록 기울기와 절편을 계산합니다.

이렇게 만들어진 직선을 이용하여 사용자가 입력한
미래 연도의 평균기온을 예측합니다.
""")

st.info(
    "그래프에서 파란 점은 실제 기온, "
    "빨간 선은 선형회귀가 계산한 예측선, "
    "주황색 별은 사용자가 선택한 연도의 예측 기온입니다. "
    "회색 점선은 실제값과 예측선 사이의 차이를 나타냅니다."
)

# --------------------------------
# 회귀 모델 정보
# --------------------------------

st.subheader("📐 선형회귀 계산 결과")

st.write(
    f"**회귀식:** y = {slope:.4f}x + {intercept:.4f}"
)

st.write(
    f"**결정계수 (R²):** {model.score(X, y):.4f}"
)

st.write(
    f"**학습 데이터 개수:** {len(month_df)}개"
)

st.caption(
    "주의: 선형회귀는 과거 데이터의 추세를 이용한 단순 예측입니다. "
    "계절 변화, 기후변화 등 다양한 요인을 모두 반영하지는 않습니다."
)
