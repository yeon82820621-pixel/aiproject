
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Seoul Travel TOP 10",
    page_icon="🇰🇷",
    layout="wide"
)

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "eng": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 왕조의 대표 궁궐입니다. 한국의 전통 건축과 역사를 경험하고 한복을 입고 사진을 찍기 좋은 장소입니다.",
        "category": "역사 · 전통문화",
        "emoji": "🏯"
    },
    {
        "name": "북촌한옥마을",
        "eng": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "아름다운 전통 한옥이 모여 있는 마을입니다. 한국의 옛 주거문화와 골목길 풍경을 감상할 수 있습니다.",
        "category": "전통문화 · 사진",
        "emoji": "🏘️"
    },
    {
        "name": "명동",
        "eng": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "desc": "서울의 대표적인 쇼핑 거리입니다. K-뷰티, 패션, 화장품과 다양한 한국 길거리 음식을 즐길 수 있습니다.",
        "category": "쇼핑 · 음식",
        "emoji": "🛍️"
    },
    {
        "name": "남산서울타워",
        "eng": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울의 전경을 한눈에 볼 수 있는 대표 전망 명소입니다. 특히 일몰과 야경이 아름답습니다.",
        "category": "전망 · 야경",
        "emoji": "🗼"
    },
    {
        "name": "광장시장",
        "eng": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9998,
        "desc": "빈대떡, 마약김밥, 육회 등 한국의 다양한 전통 음식을 맛볼 수 있는 유명한 시장입니다.",
        "category": "전통시장 · 음식",
        "emoji": "🥢"
    },
    {
        "name": "홍대거리",
        "eng": "Hongdae Street",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "K-POP, 스트리트 공연, 개성 있는 상점과 카페가 가득한 젊음과 예술의 거리입니다.",
        "category": "K-POP · 문화",
        "emoji": "🎤"
    },
    {
        "name": "동대문디자인플라자",
        "eng": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "desc": "독특한 미래형 건축물로 유명합니다. 전시회와 디자인 행사, 아름다운 야간 조명을 즐길 수 있습니다.",
        "category": "건축 · 디자인",
        "emoji": "🏢"
    },
    {
        "name": "코엑스 별마당도서관",
        "eng": "Starfield Library COEX",
        "lat": 37.5078,
        "lon": 127.0596,
        "desc": "높은 천장과 거대한 책장이 인상적인 복합문화공간입니다. 사진 촬영과 쇼핑을 함께 즐길 수 있습니다.",
        "category": "문화 · 쇼핑",
        "emoji": "📚"
    },
    {
        "name": "성수동·서울숲",
        "eng": "Seongsu-dong & Seoul Forest",
        "lat": 37.5445,
        "lon": 127.0560,
        "desc": "개성 있는 카페와 패션 편집숍, 예술 공간이 모여 있는 트렌디한 지역입니다. 서울숲에서 자연도 즐길 수 있습니다.",
        "category": "카페 · 자연",
        "emoji": "🌳"
    },
    {
        "name": "롯데월드타워 서울스카이",
        "eng": "Lotte World Tower Seoul Sky",
        "lat": 37.5125,
        "lon": 127.1025,
        "desc": "한국을 대표하는 초고층 랜드마크입니다. 전망대에서 서울의 도시 풍경과 한강을 감상할 수 있습니다.",
        "category": "랜드마크 · 전망",
        "emoji": "🌆"
    }
]

# 제목
st.title("🇰🇷 Seoul Travel TOP 10")
st.subheader("Discover the Best of Seoul, South Korea")
st.write(
    "서울을 방문하는 외국인 관광객을 위한 "
    "서울 대표 관광지 10곳을 지도에서 만나보세요."
)

st.divider()

# 지도 만들기
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="CartoDB positron"
)

# 관광지 마커 추가
for i, place in enumerate(places, start=1):

    popup_html = f"""
    <div style="width:220px">
        <h4>{i}. {place['name']}</h4>
        <b>{place['eng']}</b>
        <p>{place['desc']}</p>
        <a href="https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
           target="_blank">Google Maps 길찾기</a>
    </div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{i}. {place['name']}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#E53935;
                color:white;
                border-radius:50%;
                width:32px;
                height:32px;
                text-align:center;
                line-height:32px;
                font-weight:bold;
                border:2px solid white;
                box-shadow:0 2px 5px #888;
            ">{i}</div>
            """,
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
    ).add_to(seoul_map)

# 지도 화면
st.header("📍 Seoul Tourist Map")
st.caption("지도 위의 숫자를 클릭하면 관광지 정보를 볼 수 있습니다.")

st_folium(
    seoul_map,
    width=None,
    height=600,
    returned_objects=[],
    key="seoul_tourist_map"
)

st.divider()

# 관광지 설명
st.header("⭐ TOP 10 Tourist Attractions")
st.write("서울에서 꼭 방문해 볼 만한 대표 관광지입니다.")

for i, place in enumerate(places, start=1):

    with st.container(border=True):
        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown(f"## {i}")
            st.markdown(f"### {place['emoji']}")

        with col2:
            st.subheader(place["name"])
            st.caption(place["eng"])
            st.write(place["desc"])
            st.markdown(f"**분류:** {place['category']}")

            google_url = (
                "https://www.google.com/maps/search/?api=1"
                f"&query={place['lat']},{place['lon']}"
            )

            st.link_button(
                "📍 Google Maps에서 위치 확인",
                google_url
            )

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>❤️ Welcome to Seoul!</h3>
        <p>Experience Korean Culture, Food and Beautiful Places.</p>
        <p>© Seoul Travel TOP 10</p>
    </div>
    """,
    unsafe_allow_html=True
)
