import streamlit as st

# 페이지 설정
st.set_page_config(page_title="타이니닷 로스터리 카페", page_icon="☕", layout="wide")

# 로고 이미지 표시
st.image(r"C:\Users\wkddl\Desktop\새 폴더\logo.png", width=200)

# 제목 및 소개
st.title("타이니닷 로스터리 카페")
st.write("🌱 신선한 원두를 직접 로스팅하는 **타이니닷**에 오신 것을 환영합니다!")
st.write("📍 인천 주안에 위치한 스페셜티 로스터리 카페")

# 네비게이션
menu = st.sidebar.radio("메뉴", ["홈", "원두 구매"])

if menu == "홈":
    st.header("☕ 타이니닷 소개")
    st.write(
        """
        - 직접 로스팅한 신선한 원두를 제공합니다.
        - 스페셜티 커피를 최상의 상태로 즐길 수 있습니다.
        - 다양한 핸드드립 커피와 디저트를 만나보세요!
        """
    )

elif menu == "원두 구매":
    st.header("🛒 원두 구매")
    st.write("아래에서 원하시는 원두를 선택하고 수량을 입력하세요.")

    # 원두 옵션
    beans = ["에티오피아 예가체프", "콜롬비아 수프리모", "과테말라 안티구아"]
    choice = st.selectbox("원두 선택", beans)

    # 수량 선택
    quantity = st.number_input("구매할 수량(kg)", min_value=0.1, max_value=10.0, step=0.1)

    # 주문 버튼
    if st.button("🛍️ 주문하기"):
        if quantity > 0:
            st.success(f"✅ {choice} {quantity}kg 주문이 완료되었습니다!")
        else:
            st.warning("❗ 수량을 0보다 크게 설정하세요.")




