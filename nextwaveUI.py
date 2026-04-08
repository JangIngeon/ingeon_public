import streamlit as st

st.set_page_config(page_title="간편 가입", layout="centered")

# 스타일 (모바일 느낌 카드 UI)
st.markdown("""
<style>
.container {
    max-width: 360px;
    margin: auto;
    padding: 20px;
    border-radius: 20px;
    background-color: #ffffff;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
    text-align: center;
}

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

.login-btn {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    color: white;
    text-decoration: none;
}

.google {
    background-color: #4285F4;
}

.kakao {
    background-color: #FEE500;
    color: black;
}
</style>
""", unsafe_allow_html=True)


# 카드 시작
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown('<div class="title">간편 가입</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    "커피 한 모금 마시는 사이 가입 끝 ☕<br>"
    "당신의 소중한 시간을 10초도 뺏지 않겠습니다."
    '</div>',
    unsafe_allow_html=True
)

# 프로그레스 바 (잔여 단계 표시)
st.progress(0.3, text="가입 단계 1/3")

# 소셜 로그인 버튼
st.markdown(
    '<a class="login-btn google">Google로 시작하기</a>',
    unsafe_allow_html=True
)

st.markdown(
    '<a class="login-btn kakao">카카오로 시작하기</a>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
