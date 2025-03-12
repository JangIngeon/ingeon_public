import streamlit as st
import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

# 주문 테이블 생성 (최초 실행 시)
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    customer_id TEXT,
    address TEXT,
    bean TEXT,
    quantity REAL,
    total_price INTEGER,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# 페이지 설정
st.set_page_config(page_title="타이니닷 로스터리 카페", page_icon="☕", layout="wide")

# 네비게이션 메뉴
menu = st.sidebar.radio("메뉴", ["홈", "원두 구매", "주문 관리"])

# 로고 이미지 표시
st.image("https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20240703_21%2F1719934078338XAW2P_JPEG%2FKakaoTalk_20240703_001904553_29.jpg", width=300)

if menu == "홈":
    st.header("☕ 타이니닷 소개")
    st.write("🌱 신선한 원두를 직접 로스팅하는 **타이니닷**에 오신 것을 환영합니다!")
    st.write("직접 로스팅한 스페셜티 원두와 정성 가득한 디저트를 만나보세요.")

elif menu == "원두 구매":
    st.header("🛒 원두 구매")
    st.write("아래에서 원하시는 원두를 선택하고 정보를 입력하세요.")

    # 원두 옵션 및 가격
    bean_prices = {
        "디카페인": 15000,
        "아바야 게이샤": 15000,
        "에티오피아 예가체프": 12000,
        "에티오피아 코케허니": 12000,
        "콜롬비아 수프리모": 12000,
        "인도네시아 만델링": 12000,
        "케냐 AA": 12000,
        "과테말라 안티구아": 12000
    }

    # 고객 정보 입력
    name = st.text_input("이름")
    phone = st.text_input("전화번호", placeholder="010-1234-5678")
    customer_id = st.text_input("고객번호 (일련번호)")
    address = st.text_area("주소", placeholder="배송받을 주소를 입력하세요.")

    # 원두 선택
    beans = list(bean_prices.keys())
    choice = st.selectbox("원두 선택", beans)
    st.write(f"💰 가격: **{bean_prices[choice]}원/kg**")

    # 원두 수량
    quantity = st.number_input("구매할 수량(kg)", min_value=0.1, max_value=10.0, step=0.1)
    total_price = bean_prices[choice] * quantity

    # 주문 버튼
    if st.button("🛍️ 주문하기"):
        if name and phone and customer_id and address and quantity > 0:
            cursor.execute(
                "INSERT INTO orders (name, phone, customer_id, address, bean, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, phone, customer_id, address, choice, quantity, total_price)
            )
            conn.commit()
            st.success(f"✅ {name}님의 주문이 완료되었습니다! 총 금액: {total_price:,.0f}원")
        else:
            st.warning("❗ 모든 정보를 입력하고 수량을 0보다 크게 설정하세요.")

elif menu == "주문 관리":
    st.header("📋 주문 관리")
    st.write("고객의 주문 내역을 확인할 수 있습니다.")

    # 주문 내역 조회
    cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()

    if orders:
        st.write("📦 최근 주문 내역")
        for order in orders:
            st.write(f"""
            - **주문번호**: {order[0]}
            - **이름**: {order[1]}
            - **전화번호**: {order[2]}
            - **고객번호**: {order[3]}
            - **주소**: {order[4]}
            - **원두 종류**: {order[5]}
            - **수량**: {order[6]}kg
            - **총 금액**: {order[7]:,}원
            - **주문 날짜**: {order[8]}
            ---
            """)
    else:
        st.write("🛑 현재 주문 내역이 없습니다.")
