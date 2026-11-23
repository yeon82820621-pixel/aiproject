
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 페이지 설정
st.set_page_config(
    page_title="붓꽃 품종 예측 프로그램",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하면 붓꽃의 품종을 예측합니다.")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Iris.csv"
    df = pd.read_csv(file_path, encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # 사용할 특성과 정답 데이터
    X = df[["꽃잎길이", "꽃잎 너비"]]
    y = df["품종"]

    # KNN 모델 생성
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=5))
    ])

    # 모델 학습
    model.fit(X, y)

    # 입력 범위
    min_length = float(X["꽃잎길이"].min())
    max_length = float(X["꽃잎길이"].max())

    min_width = float(X["꽃잎 너비"].min())
    max_width = float(X["꽃잎 너비"].max())

    st.divider()

    # 입력 화면
    st.subheader("1. 꽃잎 정보 입력")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"꽃잎 길이 입력 범위: {min_length} ~ {max_length} cm"
        )

        petal_length = st.slider(
            "꽃잎 길이 (cm)",
            min_value=min_length,
            max_value=max_length,
            value=4.0,
            step=0.1
        )

    with col2:
        st.info(
            f"꽃잎 너비 입력 범위: {min_width} ~ {max_width} cm"
        )

        petal_width = st.slider(
            "꽃잎 너비 (cm)",
            min_value=min_width,
            max_value=max_width,
            value=1.0,
            step=0.1
        )

    # 예측 버튼
    if st.button("🌸 품종 예측하기", use_container_width=True):

        # 사용자 입력 데이터
        input_data = pd.DataFrame({
            "꽃잎길이": [petal_length],
            "꽃잎 너비": [petal_width]
        })

        # 품종 예측
        prediction = model.predict(input_data)[0]

        # 예측 결과
        st.divider()
        st.subheader("2. 예측 결과")

        st.success(f"예측된 붓꽃 품종: {prediction}")

        st.write(f"꽃잎 길이: {petal_length} cm")
        st.write(f"꽃잎 너비: {petal_width} cm")

        # 예측 확률
        probabilities = model.predict_proba(input_data)[0]
        classes = model.classes_

        st.write("### 품종별 예측 확률")

        probability_df = pd.DataFrame({
            "품종": classes,
            "예측 확률 (%)": probabilities * 100
        })

        st.bar_chart(
            probability_df.set_index("품종")
        )

        st.divider()
        st.subheader("3. 꽃잎 크기 분포 그래프")

        # 그래프 생성
        fig = go.Figure()

        # 품종별 데이터 표시
        for species in df["품종"].unique():

            species_data = df[df["품종"] == species]

            fig.add_trace(go.Scatter(
                x=species_data["꽃잎길이"],
                y=species_data["꽃잎 너비"],
                mode="markers",
                name=species,
                marker=dict(size=9)
            ))

        # 사용자가 입력한 위치 표시
        fig.add_trace(go.Scatter(
            x=[petal_length],
            y=[petal_width],
            mode="markers",
            name="사용자 입력 위치",
            marker=dict(
                symbol="star",
                size=25,
                color="yellow",
                line=dict(color="black", width=1.5)
            )
        ))

        # 그래프 제목 및 축 설정
        fig.update_layout(
            title="붓꽃 품종별 꽃잎 크기 분포",
            xaxis_title="꽃잎 길이 (cm)",
            yaxis_title="꽃잎 너비 (cm)",
            legend_title="붓꽃 품종",
            height=600,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "노란색 별표는 사용자가 입력한 꽃잎의 위치입니다."
        )

except FileNotFoundError:
    st.error("Iris.csv 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
