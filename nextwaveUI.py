import streamlit as st

st.set_page_config(page_title="가입 UX 데모", layout="wide")

# 스타일
st.markdown("""
<style>

/* PC 프레임 */
.pc-frame {
    width: 1000px;
    margin: 40px auto;
    padding: 20px;
    border-radius: 16px;
    background-color: #f1f3f5;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
}

/* 브라우저 상단 */
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

/* 내부 레이아웃 */
.content {
    display: flex;
    justify-content: space-between;
}

/* 모바일 UI */
.mobile {
    width: 360px;
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
}

.google {
    background-color: #4285F4;
    color: white;
}

.kakao {
    background-color: #FEE500;
    color: black;
}

/* 기획 설명 */
.idea-box {
    width: 500px;
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
    font-size: 15px;
    line-height: 1.6;
}

.idea-title {
    font-weight: bold;
    margin-bottom: 10px;
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

# 내부 컨텐츠
st.markdown('<div class="content">', unsafe_allow_html=True)

# ✅ 왼쪽: 모바일 UI
st.markdown('<div class="mobile">', unsafe_allow_html=True)

st.markdown('<div class="title">간편 가입</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    "커피 한 모금 마시는 사이 가입 끝 ☕<br>"
    "당신의 소중한 시간을 10초도 뺏지 않겠습니다."
    '</div>',
    unsafe_allow_html=True
)

st.progress(0.33, text="가입 단계 1/3")

st.markdown('<div class="btn google">Google로 시작하기</div>', unsafe_allow_html=True)
st.markdown('<div class="btn kakao">카카오로 시작하기</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ 오른쪽: 기획 문구 그대로 출력
st.markdown("""
<div class="idea-box">
<div class="idea-title">📌 가입 UX 설계 전략</div>

가입 절차를 최대한 간소화한 방식을 적용한다.<br><br>

구글·카카오 소셜 로그인 버튼을 최상단에 배치하고,<br>
실시간 프로그레스 바로 잔여 단계를 직관적으로 제시하며,<br><br>

<strong>
"커피 한 모금 마시는 사이 가입 끝.  
당신의 소중한 시간을 10초도 뺏지 않겠습니다."
</strong><br><br>

라는 문구로 인지적 저항을 낮춘다.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # content 끝
st.markdown('</div>', unsafe_allow_html=True)  # pc-frame 끝
