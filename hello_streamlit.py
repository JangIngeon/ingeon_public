import streamlit as st

# 페이지 설정
st.set_page_config(page_title="타이니닷 로스터리 카페", page_icon="☕", layout="wide")

# 네비게이션 메뉴
menu = st.sidebar.radio("메뉴", ["홈", "원두 구매"])

# 로고 이미지 표시
st.image(r"https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20240703_21%2F1719934078338XAW2P_JPEG%2FKakaoTalk_20240703_001904553_29.jpg", width=300)

if menu == "홈":
    st.header("☕ 타이니닷 소개")
    st.write(
        """
        - 직접 로스팅한 신선한 원두를 제공합니다.
        - 스페셜티 커피를 최상의 상태로 즐길 수 있습니다.
        - 다양한 핸드드립 커피와 디저트를 만나보세요!
        """
    )
    # 제목 및 소개
    st.title("타이니닷 로스터리 카페")
    st.write("🌱 신선한 원두를 직접 로스팅하는 **타이니닷**에 오신 것을 환영합니다!")
    st.write('''인천 미추홀구의 숨겨진 보석
타이니닷(Tiny dot)

주안동에 자리 잡은 특별한 카페 타이니닷(Tiny dot)은
'작지만 강한 점' 이라는 뜻을 품고, 한 잔의 커피로 하루의 쉼과 특별함을 선사합니다.
타이니닷은 단순히 커피를 파는 공간이 아니라, 미추홀구 주안에서 특별한 기억을 만들고 싶은 이들을 위한 장소입니다.

10년의 커피 노하우, 타이니닷의 시작

2014년, '카이저커피'라는 이름으로 커피 제조와 바리스타 교육에 힘써 온 타이니닷은 커피에 대한 사랑과 열정을 바탕으로 새로운 이름으로 재탄생했습니다.
타이니닷은 '모든 시작은 작은 점에서 시작한다'는 믿음으로,
커피 한 잔 한 잔에 정성과 이야기를 담아냅니다.
타이니닷은 인천 주안카페 중에서도 고객과의 감정적인 연결을 가장 소중히 여깁니다.

[타이니닷 커피 & 음료 메뉴]
매일 신선하게 로스팅된 원두로 타이니닷만의 깊은 맛을 제공합니다.
커피 전문가의 손길로 탄생한 메뉴는 음미할수록 진가를 느끼게 합니다.

- 싱글 오리진 원두 : 다양한 산지의 풍미를 그대로 담아낸 로스팅
- 블랜딩 원두 : 타이니닷만의 노하우로 완성한 최고의 밸런스
- 디카페인 원두 : 카페인이 없어도 커피의 깊은 맛을 유지
- 라떼류 : 고소하고 진한 맛으로, 우유와의 환상적인 조화

그 외에도 신선한 생과일로 만든 프레쉬 에이드 & 주스,
유기농 허브차와 대추만으로 만든 수제 대추차 등 건강하고 신선한 메뉴를 제공합니다.

[프리미엄 디저트, 타이니닷의 자부심]
인천 브런치카페 타이니닷에서는 최고급 재료로 만든 디저트를 선보입니다.
프랑스산 고메버터와 무항생제 달걀로 구워낸 부드러운 베이커리
발로나 초콜릿과 하동 말차가루로 만든 특별한 디저트

정성과 품질로 만들어진 디저트는 커피와의 완벽한 페어링을 자랑합니다.

[편안함을 선사하는 공간]
타이니닷은 층마다 다른 매력을 지닌 공간으로, 다양한 고객의 취향을 만족시킵니다.
깨끗하고 정돈된 남녀 화장실 분리 구조
단체 손님을 위한 전용 공간 : 세미나, 가족 모임, 친목 모임 등 다양한 이벤트 가능

아늑한 분위기와 세심한 배려로 주안카페 중에서도 잊을 수 없는 시간을 제공합니다.

[타이니닷이 사랑받는 이유]
1. 커피 제조 공장 운영으로 매일 신선한 원두 제공
타이니닷의 커피는 매일 직접 로스팅되어, 품질과 신선도를 모두 갖추고 있습니다.

2. 고객의 건강을 위한 디저트
첨가물을 배제하고, 자연의 맛을 살린 디저트는 아이부터 어른까지 누구나 즐길 수 있습니다.

3. 맞춤형 공간 활용
타이니닷은 단체 모임, 친구와의 수다, 혹은 혼자만의 여유에도 최적화된 공간을 제공합니다.
''')

elif menu == "원두 구매":
    st.header("🛒 원두 구매")
    st.write("아래에서 원하시는 원두를 선택하고 수량을 입력하세요.")

    # 원두 옵션 및 가격 (200g, 500g, 1kg 가격 책정)
    bean_prices = {
        "아바야 게이샤": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "에티오피아 예가체프": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "에티오피아 코케허니": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "콜롬비아 수프리모": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "인도네시아 만델링": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "케냐 AA": {"200g": 12000, "500g": 25000, "1kg": 45000},
        "과테말라 안티구아": {"200g": 12000, "500g": 25000, "1kg": 45000}
    }
    
    beans = list(bean_prices.keys())
    choice = st.selectbox("원두 선택", beans)
    selected_bean = bean_prices[choice]
    
    st.write(f"💰 가격")
    st.write(f" 200g: **{selected_bean['200g']}원**")
    st.write(f" 500g: **{selected_bean['500g']}원**")
    st.write(f" 1kg: **{selected_bean['1kg']}원**")

    # 크기 선택
    size_choice = st.selectbox("선택할 크기", ["200g", "500g", "1kg"])
    quantity = st.number_input(f"{size_choice} 수량", min_value=1, max_value=10, step=1)
    total_price = selected_bean[size_choice] * quantity

    # 주문 버튼
    if st.button("🛍️ 주문하기"):
        if quantity > 0:
            st.success(f"✅ {choice} {size_choice} {quantity}개 주문이 완료되었습니다! 총 금액: {total_price:,.0f}원")
        else:
            st.warning("❗ 수량을 1개 이상 설정하세요.")
