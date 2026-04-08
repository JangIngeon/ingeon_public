import streamlit as st

# 모바일 화면처럼 보이기 위한 CSS 설정
st.set_page_config(page_title="NextWave Mobile B-Test", layout="centered")

st.markdown("""
    <style>
    /* 모바일 프레임 느낌의 컨테이너 */
    .mobile-container {
        max-width: 375px;
        margin: auto;
        border: 8px solid #333;
        border-radius: 30px;
        padding: 20px;
        background-color: white;
        height: 667px;
        overflow-y: auto;
        font-family: 'Pretendard', sans-serif;
    }
    .stButton>button {
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        font-size: 16px;
    }
    .kakao-btn { background-color: #FEE500 !important; color: #000 !important; border: none !important; }
    .google-btn { background-color: #ffffff !important; color: #000 !important; border: 1px solid #ddd !important; }
    .highlight-box {
        background-color: #f0f7ff;
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
        border-left: 5px solid #1a4a7c;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 모바일 실험군(B) UI")
st.write("각 탭을 클릭하여 실험군 B의 모바일 화면을 확인하세요.")

tab1, tab2, tab3 = st.tabs(["가입 UX", "실무 메시지", "요금제 혜택"])

# --- Test 1. 가입 프로세스 B안 (하단 퍼널) ---
with tab1:
    st.markdown("### Test 1. 간소화된 가입 프로세스")
    st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
    st.info("💡 **가입 완료까지 10초 남았습니다**")
    st.progress(85)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("커피 한 모금 마시는 사이 가입 끝! ☕")
    st.write("소중한 시간을 10초도 뺏지 않겠습니다.")
    
    st.button("🟡 카카오로 1초 만에 시작하기")
    st.button("⚪ 구글로 계속하기")
    
    st.markdown("<br><center>또는</center><br>", unsafe_allow_html=True)
    st.text_input("이메일로 계속하기", placeholder="email@address.com")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Test 2. 초기 직장인 메시지 B안 (중단 퍼널) ---
with tab2:
    st.markdown("### Test 2. 주니어 맞춤형 베네핏")
    st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
    st.write("🌊 **NextWave**")
    st.header("사수 도움 없이도 칭찬받는 '실무 치트키'")
    
    st.markdown('''
    <div class="highlight-box">
        <b>✅ 신입 사원 1,400명이 선택</b><br>
        이미 업무 적응 시간을 절반으로 줄였습니다.
    </div>
    ''', unsafe_allow_html=True)
    
    st.success("🎁 [신규 한정] 실무 템플릿 패키지 증정")
    st.write("연봉 협상 시트부터 기획서 양식까지 한 번에!")
    
    st.button("🚀 무료로 템플릿 받고 시작하기")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Test 3. 가격 저항 제거 B안 (상단 퍼널) ---
with tab3:
    st.markdown("### Test 3. 결제 부담 제로 오퍼")
    st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
    st.write("🌊 **NextWave Premium**")
    st.subheader("커피 2잔 가격으로 얻는<br>매일 1시간의 여유 ☕", unsafe_allow_html=True)
    
    st.markdown('''
    <div style="text-align: center; margin: 20px 0;">
        <h1 style="color: #1a4a7c; margin-bottom: 0;">0원</h1>
        <p style="color: #666;">14일 무료 체험</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.warning("✅ **카드 등록 없이 바로 시작하세요**")
    st.markdown("**[제휴사 추천 전용 혜택]**<br>실무 템플릿 패키지 즉시 증정", unsafe_allow_html=True)
    
    st.button("💎 부담 없이 체험 시작하기")
    st.caption("<center>체험 종료 전 알림을 보내드려요</center>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
