
import streamlit as st
from urllib.parse import quote

# ----------------------------------------
# 페이지 설정
# ----------------------------------------
st.set_page_config(
    page_title="MBTI 책 & 영화 추천",
    page_icon="📚",
    layout="centered"
)

# ----------------------------------------
# 디자인
# ----------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #F5F3FF 0%, #FFF9F0 100%);
}
.main-title {
    text-align: center;
    font-size: 35px;
    font-weight: 900;
    color: #6046A5;
    padding-top: 10px;
}
.sub-title {
    text-align: center;
    color: #77718B;
    font-size: 16px;
    margin-bottom: 25px;
}
.section-title {
    color: #6046A5;
    font-size: 23px;
    font-weight: bold;
    margin-top: 20px;
}
.recommend-card {
    background: white;
    border-radius: 15px;
    padding: 18px;
    margin: 8px 0;
    border: 1px solid #E9E2FA;
    min-height: 125px;
}
.book-title {
    font-size: 19px;
    font-weight: bold;
    color: #49377D;
}
.movie-title {
    font-size: 19px;
    font-weight: bold;
    color: #A65348;
}
.description {
    color: #666;
    font-size: 14px;
    line-height: 1.6;
}
.footer {
    text-align: center;
    color: #888;
    padding: 25px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 도서 데이터
# ----------------------------------------
books = {
    "almond": {
        "title": "아몬드",
        "author": "손원평",
        "desc": "감정을 잘 표현하지 못하는 소년의 성장 이야기. 공감과 관계에 대해 생각해 볼 수 있어!",
        "emoji": "💗"
    },
    "momo": {
        "title": "모모",
        "author": "미하엘 엔데",
        "desc": "시간의 소중함과 진정한 행복을 알려주는 환상적인 이야기!",
        "emoji": "⏳"
    },
    "giver": {
        "title": "기억 전달자",
        "author": "로이스 로리",
        "desc": "감정과 기억이 사라진 사회를 통해 자유와 선택의 의미를 생각하게 해!",
        "emoji": "🌌"
    },
    "house": {
        "title": "순례 주택",
        "author": "유은실",
        "desc": "개성 넘치는 인물들의 이야기를 통해 가족과 삶의 의미를 유쾌하게 보여줘!",
        "emoji": "🏡"
    },
    "paint": {
        "title": "페인트",
        "author": "이희영",
        "desc": "부모를 선택할 수 있다면? 가족과 관계에 대한 흥미로운 질문을 던지는 소설!",
        "emoji": "🎨"
    },
    "letter": {
        "title": "세계를 건너 너에게 갈게",
        "author": "이꽃님",
        "desc": "시간을 넘어 주고받는 편지 속에서 발견하는 따뜻한 사랑과 감동!",
        "emoji": "💌"
    },
    "demian": {
        "title": "데미안",
        "author": "헤르만 헤세",
        "desc": "나만의 길을 찾아가는 성장 이야기. 자기 자신을 깊이 생각하게 해!",
        "emoji": "🦋"
    },
    "sea": {
        "title": "노인과 바다",
        "author": "어니스트 헤밍웨이",
        "desc": "거대한 바다에 맞서는 노인의 도전! 끈기와 용기를 배울 수 있어.",
        "emoji": "🌊"
    },
    "yuwon": {
        "title": "유원",
        "author": "백온유",
        "desc": "과거의 상처와 성장, 그리고 자신만의 삶을 찾아가는 청소년 이야기!",
        "emoji": "🌱"
    },
    "philosophy": {
        "title": "청소년을 위한 철학 에세이",
        "author": "강영계",
        "desc": "일상 속 다양한 질문을 철학적으로 생각해 보는 재미있는 책!",
        "emoji": "💡"
    }
}

# ----------------------------------------
# 영화 데이터
# ----------------------------------------
movies = {
    "totoro": {
        "title": "이웃집 토토로",
        "year": 1988,
        "director": "미야자키 하야오",
        "desc": "자연과 상상력이 가득한 따뜻한 모험! 마음이 편안해지는 영화.",
        "emoji": "🌳"
    },
    "truman": {
        "title": "트루먼 쇼",
        "year": 1998,
        "director": "피터 위어",
        "desc": "내가 믿고 있는 세상이 전부 가짜라면? 자유와 진실을 생각하게 해!",
        "emoji": "📺"
    },
    "interstellar": {
        "title": "인터스텔라",
        "year": 2014,
        "director": "크리스토퍼 놀란",
        "desc": "우주와 과학, 가족의 사랑이 어우러진 압도적인 SF 영화!",
        "emoji": "🚀"
    },
    "deadpoets": {
        "title": "죽은 시인의 사회",
        "year": 1989,
        "director": "피터 위어",
        "desc": "자신만의 꿈과 목소리를 찾는 학생들의 이야기. 카르페 디엠!",
        "emoji": "🎓"
    },
    "abouttime": {
        "title": "어바웃 타임",
        "year": 2013,
        "director": "리처드 커티스",
        "desc": "평범한 하루와 소중한 사람들의 가치를 알려주는 감성 로맨스!",
        "emoji": "❤️"
    },
    "insideout": {
        "title": "인사이드 아웃",
        "year": 2015,
        "director": "피트 닥터",
        "desc": "기쁨, 슬픔, 버럭이까지! 우리의 감정을 재미있게 이해할 수 있어.",
        "emoji": "🌈"
    },
    "hiddenfigures": {
        "title": "히든 피겨스",
        "year": 2016,
        "director": "시어도어 멜피",
        "desc": "편견을 넘어 자신의 능력을 증명한 여성 수학자들의 실화!",
        "emoji": "🧮"
    },
    "littleforest": {
        "title": "리틀 포레스트",
        "year": 2018,
        "director": "임순례",
        "desc": "자연 속에서 자신을 돌아보는 힐링 영화. 맛있는 음식은 덤!",
        "emoji": "🍃"
    },
    "coco": {
        "title": "코코",
        "year": 2017,
        "director": "리 언크리치",
        "desc": "음악과 가족, 기억에 관한 아름다운 애니메이션!",
        "emoji": "🎸"
    },
    "goodwill": {
        "title": "굿 윌 헌팅",
        "year": 1997,
        "director": "구스 반 산트",
        "desc": "천재 청년이 진정한 자신을 찾아가는 감동적인 이야기!",
        "emoji": "🧠"
    },
    "martian": {
        "title": "마션",
        "year": 2015,
        "director": "리들리 스콧",
        "desc": "화성에 홀로 남겨진 과학자의 생존 프로젝트! 문제 해결의 재미가 가득해.",
        "emoji": "🪐"
    },
    "soul": {
        "title": "소울",
        "year": 2020,
        "director": "피트 닥터",
        "desc": "인생의 목적과 일상의 행복에 대해 생각하게 하는 애니메이션!",
        "emoji": "🎹"
    },
    "spiderverse": {
        "title": "스파이더맨: 뉴 유니버스",
        "year": 2018,
        "director": "밥 퍼시케티 외",
        "desc": "개성 넘치는 히어로들의 화려한 액션과 성장 이야기!",
        "emoji": "🕷️"
    },
    "pursuit": {
        "title": "행복을 찾아서",
        "year": 2006,
        "director": "가브리엘 무치노",
        "desc": "어려움 속에서도 꿈을 포기하지 않는 아버지의 감동 실화!",
        "emoji": "🌟"
    },
    "grandbudapest": {
        "title": "그랜드 부다페스트 호텔",
        "year": 2014,
        "director": "웨스 앤더슨",
        "desc": "독특한 색감과 유머, 개성 넘치는 캐릭터가 돋보이는 작품!",
        "emoji": "🏨"
    },
    "paddington": {
        "title": "패딩턴",
        "year": 2014,
        "director": "폴 킹",
        "desc": "귀여운 곰 패딩턴의 따뜻하고 유쾌한 런던 적응기!",
        "emoji": "🐻"
    }
}

# ----------------------------------------
# MBTI 유형별 추천
# ----------------------------------------
mbti_data = {
    "ISTJ": {
        "name": "청렴결백한 현실주의자",
        "emoji": "📋",
        "intro": "차근차근 목표를 이루는 책임감 강한 계획가!",
        "books": ["giver", "sea"],
        "movies": ["hiddenfigures", "martian"]
    },
    "ISFJ": {
        "name": "용감한 수호자",
        "emoji": "🧸",
        "intro": "주변 사람들을 세심하게 챙기는 따뜻한 마음의 소유자!",
        "books": ["almond", "letter"],
        "movies": ["abouttime", "paddington"]
    },
    "INFJ": {
        "name": "선의의 옹호자",
        "emoji": "🌙",
        "intro": "깊은 생각과 따뜻한 공감 능력을 가진 이상주의자!",
        "books": ["demian", "almond"],
        "movies": ["soul", "deadpoets"]
    },
    "INTJ": {
        "name": "용의주도한 전략가",
        "emoji": "♟️",
        "intro": "큰 그림을 그리며 논리적으로 미래를 설계하는 전략가!",
        "books": ["giver", "philosophy"],
        "movies": ["interstellar", "truman"]
    },
    "ISTP": {
        "name": "만능 재주꾼",
        "emoji": "🔧",
        "intro": "직접 경험하고 문제를 해결하는 것을 좋아하는 탐험가!",
        "books": ["sea", "giver"],
        "movies": ["martian", "spiderverse"]
    },
    "ISFP": {
        "name": "호기심 많은 예술가",
        "emoji": "🎨",
        "intro": "자유로운 감성과 자신만의 취향을 소중히 여기는 예술가!",
        "books": ["momo", "letter"],
        "movies": ["littleforest", "totoro"]
    },
    "INFP": {
        "name": "열정적인 중재자",
        "emoji": "🦋",
        "intro": "상상력이 풍부하고 자신만의 가치관을 소중히 여기는 몽상가!",
        "books": ["demian", "momo"],
        "movies": ["coco", "soul"]
    },
    "INTP": {
        "name": "논리적인 사색가",
        "emoji": "🔬",
        "intro": "새로운 지식을 탐구하고 세상의 원리를 궁금해하는 호기심 왕!",
        "books": ["philosophy", "giver"],
        "movies": ["interstellar", "goodwill"]
    },
    "ESTP": {
        "name": "모험을 즐기는 사업가",
        "emoji": "🏄",
        "intro": "일단 도전하고 행동하는 에너지 넘치는 모험가!",
        "books": ["sea", "house"],
        "movies": ["spiderverse", "martian"]
    },
    "ESFP": {
        "name": "자유로운 연예인",
        "emoji": "🎉",
        "intro": "즐거운 분위기를 만들고 순간을 즐길 줄 아는 인기쟁이!",
        "books": ["house", "almond"],
        "movies": ["paddington", "coco"]
    },
    "ENFP": {
        "name": "재기발랄한 활동가",
        "emoji": "🌈",
        "intro": "새로운 아이디어와 가능성을 발견하는 열정적인 상상가!",
        "books": ["momo", "letter"],
        "movies": ["grandbudapest", "spiderverse"]
    },
    "ENTP": {
        "name": "뜨거운 논쟁을 즐기는 변론가",
        "emoji": "⚡",
        "intro": "기발한 생각과 토론을 즐기는 아이디어 발전소!",
        "books": ["philosophy", "paint"],
        "movies": ["truman", "goodwill"]
    },
    "ESTJ": {
        "name": "엄격한 관리자",
        "emoji": "🏆",
        "intro": "목표를 세우고 체계적으로 이끄는 든든한 리더!",
        "books": ["sea", "yuwon"],
        "movies": ["pursuit", "hiddenfigures"]
    },
    "ESFJ": {
        "name": "사교적인 외교관",
        "emoji": "🌷",
        "intro": "사람들과 함께하는 시간을 좋아하는 따뜻한 분위기 메이커!",
        "books": ["house", "letter"],
        "movies": ["abouttime", "coco"]
    },
    "ENFJ": {
        "name": "정의로운 사회운동가",
        "emoji": "🌟",
        "intro": "사람들에게 긍정적인 영향을 주고 함께 성장하는 리더!",
        "books": ["almond", "paint"],
        "movies": ["deadpoets", "pursuit"]
    },
    "ENTJ": {
        "name": "대담한 통솔자",
        "emoji": "👑",
        "intro": "목표를 향해 거침없이 나아가는 자신감 넘치는 리더!",
        "books": ["demian", "philosophy"],
        "movies": ["hiddenfigures", "interstellar"]
    }
}

# ----------------------------------------
# 화면 구성
# ----------------------------------------
st.markdown(
    '<div class="main-title">📚 MBTI 책 & 영화 추천 🎬</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">나의 MBTI와 찰떡궁합인 책과 영화를 만나보자!</div>',
    unsafe_allow_html=True
)

st.markdown("### 🧩 나의 MBTI를 선택해 줘!")

selected = st.selectbox(
    "MBTI 유형 선택",
    list(mbti_data.keys()),
    format_func=lambda x: f"{x} - {mbti_data[x]['name']}"
)

# 선택한 유형 데이터
personality = mbti_data[selected]

st.markdown("---")

# 성격 소개
st.markdown(
    f"""
    <div style="
        background: white;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        border: 2px solid #DDD1FA;">
        <div style="font-size: 45px;">{personality['emoji']}</div>
        <h2 style="color:#6046A5;">{selected}</h2>
        <h3 style="color:#555;">{personality['name']}</h3>
        <p style="color:#777;">{personality['intro']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------
# 책 추천
# ----------------------------------------
st.markdown(
    '<div class="section-title">📖 너에게 추천하는 책 2권</div>',
    unsafe_allow_html=True
)

book_cols = st.columns(2)

for i, book_id in enumerate(personality["books"]):
    book = books[book_id]
    search_url = (
        "https://www.yes24.com/Product/Search?"
        "domain=ALL&query=" + quote(book["title"])
    )

    with book_cols[i]:
        st.markdown(
            f"""
            <div class="recommend-card">
                <div style="font-size:30px;">{book['emoji']}</div>
                <div class="book-title">{book['title']}</div>
                <p style="color:#888;">✍️ {book['author']}</p>
                <div class="description">{book['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.link_button(
            "📚 예스24에서 책 보기",
            search_url,
            use_container_width=True
        )

# ----------------------------------------
# 영화 추천
# ----------------------------------------
st.markdown(
    '<div class="section-title">🎬 너에게 추천하는 영화 2편</div>',
    unsafe_allow_html=True
)

movie_cols = st.columns(2)

for i, movie_id in enumerate(personality["movies"]):
    movie = movies[movie_id]

    with movie_cols[i]:
        st.markdown(
            f"""
            <div class="recommend-card">
                <div style="font-size:30px;">{movie['emoji']}</div>
                <div class="movie-title">{movie['title']}</div>
                <p style="color:#888;">
                    🎞️ {movie['year']}년 · {movie['director']}
                </p>
                <div class="description">{movie['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------------------
# 마무리
# ----------------------------------------
st.markdown("---")

st.markdown(
    """
    <div style="
        background:#EEE8FF;
        border-radius:15px;
        padding:20px;
        text-align:center;">
        <h3 style="color:#6046A5;">💜 오늘의 추천이 마음에 들었나요?</h3>
        <p style="color:#666;">
        책 한 권, 영화 한 편이 새로운 나를 발견하는 계기가 될 수 있어!
        </p>
        <p style="font-size:25px;">📚 🍿 ✨ 🌈</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="footer">'
    'MBTI 책 & 영화 추천 서비스 | 재미로 즐기는 성격별 추천 💜'
    '<br>※ MBTI는 성격을 완벽하게 규정하는 기준이 아니며, 추천은 참고용입니다.'
    '</div>',
    unsafe_allow_html=True
)
