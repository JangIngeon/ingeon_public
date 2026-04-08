import streamlit as st

# 페이지 설정
st.set_page_config(page_title="NextWave Mobile UX Prototype", layout="centered")

# 스마트폰 프레임 및 모바일 UI 스타일링
st.markdown("""
    <style>
    /* 스마트폰 외부 베젤 */
    .iphone-frame {
        width: 360px;
        height: 740px;
        margin: auto;
        border: 12px solid #222;
        border-radius: 45px;
        padding: 15px;
        background-color: white;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    /* 상단 스피커 구멍 */
    .iphone-frame::before {
        content: "";
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 5px;
        background-color: #333;
        border-radius: 10px;
    }

    /* 상단 상태바 */
    .status-bar {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        padding: 5px 10px;
        margin-bottom: 20px;
    }

    /* 실험군 B 핵심 요소: 프로그레스 바 */
    .progress-section {
        margin-top: 30px;
        text-align: center;
    }
    
    .main-copy {
        font-size: 22px;
        font-weight: 800;
        line-height: 1.4;
        margin: 30px 0 10px 0;
        text-align: center;
        color: #1a4a7c;
    }
    
    .sub-copy {
        font-size: 14px;
        color: #666;
        text-align: center;
        margin-bottom: 40px;
    }

    /* 소셜 로그인 버튼 스타일 */
    .stButton>button {
        width: 100%;
        height: 55px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 12px;
        transition: 0.3s;
    }
    
    .kakao-btn button {
        background-color: #FEE500 !important;
        color: #3c1e1e !important;
        border: none !important;
    }
    
    .google-btn button {
        background-color: white !important;
        color: #555 !important;
        border: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 스마트폰 화면 시작
st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)

# 1. 상태바
st.markdown("""
    <div class="status-bar">
        <span>9:41</span>
        <span>📶 🔋</span>
    </div>
    """, unsafe_allow_html=True)

# 2. 프로그레스 바 (Test 1 핵심 요소)
st.markdown('<div class="progress-section">', unsafe_allow_html=True)
st.progress(85) # 85% 완료 상태 시각화
st.caption("가입 완료까지 단 10초 남았습니다! (85%)")
st.markdown('</div>', unsafe_allow_html=True)

# 3. 메인 카피 (Test 1 문구 반영)
st.markdown("""
    <div class="main-copy">
        커피 한 모금 마시는 사이<br>가입 끝! ☕
    </div>
    <div class="sub-copy">
        당신의 소중한 시간을<br>10초도 뺏지 않겠습니다.
    </div>
    """, unsafe_allow_html=True)

# 4. 소셜 로그인 버튼 (Test 1 최상단 배치 전략)
st.markdown('<div class="kakao-btn">', unsafe_allow_html=True)
if st.button("🟡 카카오로 1초 만에 시작하기"):
    st.balloons()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="google-btn">', unsafe_allow_html=True)
st.button("⚪ 구글로 계속하기")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><center style='color:#999; font-size:12px;'>또는</center><br>", unsafe_allow_html=True)

# 5. 기존 이메일 가입 (하단으로 밀어냄)
st.text_input("이메일 주소", placeholder="example@nextwave.com")
st.caption("※ 별도의 인증 없이 즉시 시작 가능합니다.")

st.markdown('</div>', unsafe_allow_html=True) # 스마트폰 화면 끝

# 사이드바 설명
st.sidebar.title("실험군 B 설계 포인트")
st.sidebar.markdown(f"""
- **목표:** 최종 이탈률 71.9% 방어
- **핵심 장치:**
    1. **프로그레스 바:** 잔여 단계를 직관적으로 제시 
    2. **소셜 로그인:** 최상단 배치를 통한 인증 절차 간소화 
    3. **마이크로 카피:** '10초', '커피 한 모금' 등 인지적 저항 감소 
""")
