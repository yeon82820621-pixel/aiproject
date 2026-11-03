
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Seoul Travel TOP 10",
    page_icon="🇰🇷",
    layout="wide"
)

places = [
    ("경복궁", "Gyeongbokgung Palace", 37.5796, 126.9770,
     "조선 왕조의 대표 궁궐입니다. 한국의 전통문화와 역사를 경험하세요.", "🏯"),
    ("북촌한옥마을", "Bukchon Hanok Village", 37.5826, 126.9830,
     "아름다운 한옥과 전통 골목길을 감상할 수 있습니다.", "🏘️"),
    ("명동", "Myeongdong", 37.5636, 126.9869,
     "한국 화장품, 패션, 쇼핑과 길거리 음식을 즐겨보세요.", "🛍️"),
    ("남산서울타워", "N Seoul Tower", 37.5512, 126.9882,
     "서울의 아름다운 전망과 야경을 감상할 수 있습니다.", "🗼"),
    ("광장시장", "Gwangjang Market", 37.5700, 126.9998,
     "빈대떡, 김밥, 육회 등 한국 전통음식을 맛볼 수 있습니다.", "🥢"),
    ("홍대거리", "Hongdae Street", 37.5563, 126.9236,
     "K-POP과 거리공연, 개성 있는 카페를 즐길 수 있습니다.", "🎤"),
    ("동대문디자인플라자", "DDP", 37.5671, 127.0095,
     "독특한 건축물과 다양한 전시를 경험할 수 있습니다.", "🏢"),
    ("별마당도서관", "Starfield Library", 37.5078, 127.0596,
     "거대한 책장과 아름다운 실내 공간으로 유명합니다.", "📚"),
    ("성수동·서울숲", "Seongsu & Seoul Forest", 37.5445, 127.0560,
     "트렌디한 카페와 편집숍, 자연을 즐길 수 있습니다.", "🌳"),
    ("롯데월드타워", "Lotte World Tower", 37.5125, 127.1025,
     "서울의 스카이라인과 한강을 감상할 수 있습니다.", "🌆")
]

st.title("🇰🇷 SEOUL TRAVEL TOP 10")
st.subheader("Discover Beautiful Seoul")
st.write("외국인 관광객을 위한 서울 대표 관광지 안내")

st.divider()

st.header("📍 서울 관광지 인터랙티브 지도")

# API 키가 필요 없는 OpenStreetMap 사용
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

for i, place in enumerate(places, 1):
    name, eng, lat, lon, desc, emoji = place

    popup = f"""
    <div style="width:220px">
        <h3>{emoji} {name}</h3>
        <b>{eng}</b>
        <p>{desc}</p>
        <a href="https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        target="_blank">Google Maps 위치 보기</a>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        tooltip=f"{i}. {name}",
        popup=folium.Popup(popup, max_width=300),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#e53935;
                color:white;
                width:32px;
                height:32px;
                line-height:32px;
                border-radius:50%;
                text-align:center;
                font-weight:bold;
                border:2px solid white;
                box-shadow:0 2px 5px #777;">
                {i}
            </div>
            """,
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
    ).add_to(m)

# 지도 출력
st_folium(
    m,
    width=None,
    height=600,
    returned_objects=[],
    key="seoul_travel_map"
)

st.divider()

st.header("⭐ 서울 관광지 TOP 10")

for i, place in enumerate(places, 1):
    name, eng, lat, lon, desc, emoji = place

    with st.container(border=True):
        st.subheader(f"{i}. {emoji} {name}")
        st.caption(eng)
        st.write(desc)

        url = (
            f"https://www.google.com/maps/search/"
            f"?api=1&query={lat},{lon}"
        )

        st.link_button("📍 관광지 위치 확인", url)

st.divider()

st.markdown(
    """
    <div style="text-align:center">
        <h2>❤️ Welcome to Seoul!</h2>
        <p>Enjoy Korean Culture, Food and Travel.</p>
        <p>Seoul Travel TOP 10</p>
    </div>
    """,
    unsafe_allow_html=True
)
