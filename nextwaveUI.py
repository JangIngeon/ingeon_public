import streamlit as st

st.set_page_config(page_title="가입 UI", layout="wide")

# 전체 스타일
st.markdown("""
<style>

/* PC 화면 (브라우저 프레임 느낌) */
.pc-frame {
    width: 900px;
    margin: 50px auto;
    padding: 20px;
    border-radius: 16px;
    background-color: #f1f3f5;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
}

/* 상단 브라우저 바 */
.browser-bar {
    display: flex;
    align-items: center;
    padding: 10px;
    border-radius: 10px;
    background-color: #e9ecef;
    margin-bottom: 20px;
}

.dot {
    height: 12px;
    width: 12px;
    border-radius: 50%;
    margin-right: 6px;
}

.red { background-color: #ff5f56; }
.yellow { background-color: #ffbd2e; }
.green { background-color: #27c93f; }

/* 모바일 카드 */
.mobile-container {
    width: 360px;
    margin: auto;
    padding: 25px;
    border-radius: 25px;
    background-color: white;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
    text-align: center;
}

/* 텍스트 */
.title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 14px;
    color: #666;
    margin-bottom: 20px;
}

/* 버튼 */
.btn {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
}

.google {
    background-color: #4285F4;
    color: white;
}

.kakao {
    background-color: #FEE500;
    color: black;
}

</style>
""", unsafe_allow_html=True)


# PC 프레임 시작
st.markdown('<div class="pc-frame">', unsafe_allow_html=True)

# 브라우저 바
st.markdown("""
<div class="browser-bar">
    <div class="dot red"></div>
    <div class="dot yellow"></div>
    <div class="dot green"></div>
</div>
""", unsafe_allow_html=True)

# 모바일 UI
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)

st.markdown('<div class="title">간편 가입</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    "커피 한 모금 마시는 사이 가입 끝 ☕<br>"
    "당신의 소중한 시간을 10초도 뺏지 않겠습니다."
    '</div>',
    unsafe_allow_html=True
)

# 프로그레스 바
st.progress(0.33, text="가입 단계 1/3")

# 로그인 버튼
st.markdown('<div class="btn google">Google로 시작하기</div>', unsafe_allow_html=True)
st.markdown('<div class="btn kakao">카카오로 시작하기</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 모바일 끝
st.markdown('</div>', unsafe_allow_html=True)  # PC 끝
