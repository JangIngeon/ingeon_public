import streamlit as st

st.set_page_config(layout="wide")

# 기본 padding 제거 (핵심)
st.markdown("""
<style>
.block-container {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# 전체를 브라우저처럼 렌더링
st.markdown("""
<style>

/* 전체 배경 */
body {
    background-color: #111;
}

/* 브라우저 프레임 */
.browser {
    width: 95%;
    margin: 30px auto;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    background: white;
}

/* 상단 바 */
.browser-header {
    height: 50px;
    background: #e9ecef;
    display: flex;
    align-items: center;
    padding: 0 15px;
}

/* 버튼 3개 */
.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 6px;
}
.red { background: #ff5f56; }
.yellow { background: #ffbd2e; }
.green { background: #27c93f; }

/* 주소창 느낌 */
.address-bar {
    margin-left: 10px;
    padding: 5px 10px;
    background: white;
    border-radius: 6px;
    font-size: 12px;
    color: #888;
}

/* 실제 페이지 영역 */
.page {
    padding: 40px;
}

/* 가입 UI */
.title {
    font-size: 26px;
    font-weight: bold;
}

.subtitle {
    margin-top: 8px;
    color: #666;
    font-size: 14px;
}

/* 버튼 */
.btn {
    width: 100%;
    padding: 14px;
    margin-top: 15px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}

.google {
    background: #4a7bdc;
    color: white;
}

.kakao {
    background: #ffe100;
    color: black;
}

</style>

<div class="browser">

    <div class="browser-header">
        <div class="dot red"></div>
        <div class="dot yellow"></div>
        <div class="dot green"></div>
        <div class="address-bar">https://signup.service.com</div>
    </div>

    <div class="page">

        <div class="title">간편 가입</div>

        <div class="subtitle">
        커피 한 모금 마시는 사이 가입 끝 ☕<br>
        당신의 소중한 시간을 10초도 뺏지 않겠습니다.
        </div>

    </div>
</div>
""", unsafe_allow_html=True)


# 👉 프로그레스 바는 HTML 밖에서 (Streamlit 컴포넌트라 분리)
st.progress(0.35, text="가입 단계 1/3")

# 버튼도 자연스럽게 이어지게
st.markdown("""
<div class="browser" style="margin-top:-20px;">
    <div class="page">

        <div class="btn google">Google로 시작하기</div>
        <div class="btn kakao">카카오로 시작하기</div>

    </div>
</div>
""", unsafe_allow_html=True)
