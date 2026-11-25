
import streamlit as st

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(
    page_title="MBTI 운동 추천",
    page_icon="🏃",
    layout="centered"
)

# -------------------------------
# 디자인
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #E8F5FF, #F5EDFF);
}
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: #4056A1;
}
.sub-title {
    text-align: center;
    color: #777;
    font-size: 16px;
}
.result-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    border: 2px solid #DCE5FF;
    margin-top: 15px;
}
.exercise-name {
    font-size: 30px;
    font-weight: bold;
    color: #4056A1;
}
.description {
    color: #555;
    font-size: 16px;
    line-height: 1.8;
}
.footer {
    text-align: center;
    color: #888;
    padding: 25px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# MBTI 운동 추천 데이터
# -------------------------------
exercise_data = {
    "ISTJ": {
        "name": "웨이트 트레이닝 🏋️",
        "reason": "계획적이고 꾸준한 성향에 잘 어울리는 운동이야!",
        "description": "정해진 운동 순서와 목표를 세우고 차근차근 실천해 봐.",
        "tip": "처음에는 가벼운 무게로 정확한 자세부터 익혀 보자.",
        "time": "20~30분"
    },
    "ISFJ": {
        "name": "요가 🧘",
        "reason": "차분하게 자신을 돌보고 마음의 안정을 찾는 데 좋아!",
        "description": "호흡과 스트레칭을 통해 몸과 마음을 편안하게 만들어 봐.",
        "tip": "무리하지 말고 편안한 자세부터 시작해 봐.",
        "time": "15~20분"
    },
    "INFJ": {
        "name": "등산 🏔️",
        "reason": "자연 속에서 생각을 정리하고 에너지를 충전하기 좋아!",
        "description": "자연을 느끼며 천천히 산길을 걸어 보자.",
        "tip": "처음에는 낮고 완만한 산책로를 선택해 봐.",
        "time": "30~60분"
    },
    "INTJ": {
        "name": "수영 🏊",
        "reason": "자신만의 목표를 세우고 기록을 관리하기 좋은 운동이야!",
        "description": "영법과 거리 등 작은 목표를 정해 도전해 봐.",
        "tip": "안전한 수영장에서 기본 자세부터 배워 보자.",
        "time": "20~30분"
    },
    "ISTP": {
        "name": "클라이밍 🧗",
        "reason": "문제를 해결하고 직접 도전하는 재미가 가득해!",
        "description": "다양한 홀드를 이용해 벽을 오르는 스포츠야.",
        "tip": "전문 강사의 안내에 따라 쉬운 코스부터 도전하자.",
        "time": "30~40분"
    },
    "ISFP": {
        "name": "댄스 🎵",
        "reason": "음악과 움직임으로 자유롭게 개성을 표현할 수 있어!",
        "description": "좋아하는 음악에 맞춰 춤을 추며 스트레스를 풀어 보자.",
        "tip": "좋아하는 노래 한 곡에 맞춰 자유롭게 움직여 봐.",
        "time": "15~30분"
    },
    "INFP": {
        "name": "자전거 타기 🚴",
        "reason": "자유롭게 풍경을 즐기면서 자신만의 시간을 가질 수 있어!",
        "description": "공원이나 자전거 도로에서 여유롭게 달려 보자.",
        "tip": "안전모를 착용하고 안전한 자전거 도로를 이용하자.",
        "time": "20~40분"
    },
    "INTP": {
        "name": "배드민턴 🏸",
        "reason": "전략과 순발력, 새로운 기술을 익히는 재미가 있어!",
        "description": "상대방의 움직임을 파악하고 셔틀콕을 주고받아 보자.",
        "tip": "기본 스텝과 라켓 잡는 방법부터 연습해 봐.",
        "time": "20~30분"
    },
    "ESTP": {
        "name": "농구 🏀",
        "reason": "활동적이고 역동적인 에너지를 발산하기 딱 좋아!",
        "description": "드리블과 패스, 슛을 연습하며 경기를 즐겨 보자.",
        "tip": "친구들과 가벼운 슛 연습부터 시작해 봐.",
        "time": "30~40분"
    },
    "ESFP": {
        "name": "줌바 댄스 💃",
        "reason": "신나는 음악과 함께 즐겁게 움직일 수 있는 운동이야!",
        "description": "음악에 맞춰 다양한 동작을 따라 하며 즐겨 보자.",
        "tip": "초보자용 영상을 보면서 천천히 따라 해 봐.",
        "time": "20~30분"
    },
    "ENFP": {
        "name": "인라인 스케이트 🛼",
        "reason": "새로운 경험과 자유로운 활동을 즐기는 데 잘 어울려!",
        "description": "균형을 잡고 시원하게 움직이며 새로운 재미를 느껴 봐.",
        "tip": "헬멧과 보호대를 착용하고 평탄한 장소에서 연습하자.",
        "time": "20~30분"
    },
    "ENTP": {
        "name": "탁구 🏓",
        "reason": "빠른 판단력과 창의적인 전략을 발휘할 수 있어!",
        "description": "상대의 움직임에 따라 다양한 기술을 활용해 보자.",
        "tip": "서브와 기본 랠리부터 연습해 봐.",
        "time": "20~30분"
    },
    "ESTJ": {
        "name": "달리기 🏃",
        "reason": "목표 거리와 시간을 정하고 꾸준히 도전하기 좋아!",
        "description": "자신의 페이스에 맞춰 달리며 기록을 조금씩 관리해 봐.",
        "tip": "걷기와 가벼운 달리기를 번갈아 시작해 봐.",
        "time": "20~30분"
    },
    "ESFJ": {
        "name": "배구 🏐",
        "reason": "친구들과 협력하고 함께 목표를 이루는 재미가 있어!",
        "description": "서로 공을 주고받으며 팀워크를 키워 보자.",
        "tip": "친구들과 토스와 언더패스부터 연습해 봐.",
        "time": "30~40분"
    },
    "ENFJ": {
        "name": "그룹 에어로빅 🤸",
        "reason": "다른 사람들과 함께 에너지를 나누고 운동하기 좋아!",
        "description": "여러 사람과 음악에 맞춰 다양한 동작을 해 보자.",
        "tip": "초보자 수업에서 기본 동작부터 배워 보자.",
        "time": "20~30분"
    },
    "ENTJ": {
        "name": "서킷 트레이닝 💪",
        "reason": "목표를 정하고 여러 운동을 체계적으로 진행하기 좋아!",
        "description": "스쿼트, 플랭크, 제자리 걷기 등을 순서대로 실천해 봐.",
        "tip": "처음에는 각 동작을 짧게 하고 충분히 쉬어 가자.",
        "time": "15~20분"
    }
}

# -------------------------------
# 메인 화면
# -------------------------------
st.markdown(
    '<div class="main-title">🏃 MBTI 운동 추천 💪</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '나의 MBTI와 찰떡궁합인 운동은 무엇일까?'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.markdown("### 🧩 나의 MBTI를 선택해 줘!")

mbti = st.selectbox(
    "MBTI 유형",
    list(exercise_data.keys()),
    format_func=lambda x: f"{x} 유형"
)

# -------------------------------
# 추천 결과
# -------------------------------
data = exercise_data[mbti]

st.markdown("---")
st.markdown("### 🎉 너에게 어울리는 운동은?")

st.markdown(
    f"""
    <div class="result-card">
        <div style="font-size:55px;">🏆</div>
        <div class="exercise-name">{data['name']}</div>
        <br>
        <div style="font-size:17px; color:#777;">
            {mbti} 유형 추천 운동
        </div>
        <br>
        <div class="description">
            {data['reason']}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 💡 이 운동이 어울리는 이유")

st.info(data["description"])

st.markdown("### 🔥 운동 꿀팁")

st.success(data["tip"])

st.markdown(
    f"⏰ **추천 운동 시간:** {data['time']}"
)

st.markdown("---")

st.markdown(
    """
    <div style="
        background:#E6EFFF;
        padding:20px;
        border-radius:15px;
        text-align:center;">
        <h3 style="color:#4056A1;">🌟 오늘부터 시작해 볼까?</h3>
        <p style="color:#555;">
        완벽하게 하는 것보다 즐겁게 꾸준히 하는 게 중요해!
        </p>
        <div style="font-size:30px;">🏃‍♀️ 💪 🏆</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
    MBTI 운동 추천 서비스 💙
    <br>
    ※ MBTI별 운동 추천은 재미를 위한 참고 자료이며,
    실제 운동 취향과 능력은 사람마다 달라요.
    <br>
    ※ 운동은 자신의 체력에 맞게 안전하게 진행하세요.
    </div>
    """,
    unsafe_allow_html=True
)
