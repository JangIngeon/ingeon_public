import streamlit as st

# 페이지 설정 (중앙 정렬)
st.set_page_config(page_title="NextWave 리얼 모바일 프로토타입", layout="centered")

# --- CSS 스타일링 (스마트폰 프레임 및 내부 UI) ---
st.markdown("""
    <style>
    /* 전체 배경을 어둡게 하여 스마트폰을 강조 */
    .stApp {
        background-color: #2b2b2b;
    }

    /* 스마트폰 외부 베젤 (아이폰 느낌) */
    .iphone-frame {
        width: 360px;
        height: 760px;
        margin: 40px auto;
        border: 14px solid #111; /* 두꺼운 베젤 */
        border-radius: 50px;
        padding: 10px;
        background-color: black;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        position: relative;
        overflow: hidden; /* 영역 밖 내용 숨김 */
        display: flex;
        flex-direction: column;
    }
    
    /* 상단 노치 (스피커 및 카메라 부위) */
    .iphone-frame::before {
        content: "";
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 25px;
        background-color: #111;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
        z-index: 10;
    }

    /* 스마트폰 내부 화면 영역 (실제 대조군/실험군 UI가 그려지는 곳) */
    .phone-screen {
        width: 100%;
        height: 100%;
        background-color: white; /* 화면 백그라운드 */
        border-radius: 35px;
        overflow-y: auto; /* 세로 스크롤 가능 */
        display: flex;
        flex-direction: column;
        padding: 20px;
        font-family: 'Pretendard', sans-serif;
    }

    /* 상단 상태바 */
    .status-bar {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        color: black;
        padding: 5px 15px 0 15px;
        margin-bottom: 20px;
        z-index: 5; /* 노치보다 아래 */
    }

    /* --- 내부 UI 요소 스타일 (B 실험군) --- */
    
    /* 프로그레스 바 섹션 */
    .progress-section {
        margin-top: 10px;
        text-align: center;
    }
    .progress-text {
        font-size: 12px;
        color: #666;
        margin-top: 5px;
    }
    
    /* 메인 카피 */
    .main-copy {
        font-size: 20px;
        font-weight: 800;
        line-height: 1.4;
        margin: 35px 0 10px 0;
        text-align: center;
        color: #1a4a7c;
    }
    
    /* 서브 카피 */
    .sub-copy {
        font-size: 13px;
        color: #555;
        text-align: center;
        margin-bottom: 35px;
        line-height: 1.5;
    }

    /* 소셜 로그인 버튼 공통 스타일 */
    .stButton>button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 12px;
        border: none;
        transition: transform 0.1s;
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* 카카오 버튼 (B안 핵심) */
    .kakao-btn button {
        background-color: #FEE500 !important;
        color: #3c1e1e !important;
    }
    
    /* 구글 버튼 */
    .google-btn button {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }
    
    /* 하단 이메일 입력 영역 */
    .email-section {
        margin-top: 15px;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 스마트폰 프로토타입 구현 ---

st.write("<br>", unsafe_allow_html=True) # 상단 여백

# 폰 베젤 시작
st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)

# 폰 화면 시작
st.markdown('<div class="phone-screen">', unsafe_allow_html=True)

# 1. 상단 상태바
st.markdown("""
    <div class="status-bar">
        <span>9:41</span>
        <span>📶 🔋</span>
    </div>
    """, unsafe_allow_html=True)

# 2. 프로그레스 바 Section (Test 1 B안 핵심 요소)
st.markdown('<div class="progress-section">', unsafe_allow_html=True)
# 85% 완료 상태 시각화
st.progress(85) 
st.markdown('<div class="progress-text">가입 완료까지 단 10초 남았습니다! (85%)</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 3. 메인 및 서브 카피 (인지적 저항 감소 문구 반영)
st.markdown("""
    <div class="main-copy">
        커피 한 모금 마시는 사이<br>가입 끝! ☕
    </div>
    <div class="sub-copy">
        당신의 소중한 시간을<br>10초도 뺏지 않겠습니다.
    </div>
    """, unsafe_allow_html=True)

# 4. 소셜 로그인 버튼 Section (인증 간소화 전략)
st.markdown('<div class="kakao-btn">', unsafe_allow_html=True)
if st.button("🟡 카카오로 1초 만에 시작하기"):
    # 버튼 클릭 시 퍼포먼스 (간단한 상호작용)
    st.balloons() 
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="google-btn">', unsafe_allow_html=True)
st.button("⚪ 구글로 계속하기")
st.markdown('</div>', unsafe_allow_html=True)

# 구분선 (또는)
st.markdown("<center style='color:#bbb; font-size:12px; margin: 15px 0;'>또는</center>", unsafe_allow_html=True)

# 5. 기존 이메일 가입 영역 (하단 배치)
st.markdown('<div class="email-section">', unsafe_allow_html=True)
# 입력 폼 스타일 폰트 크기 조정
st.markdown("<div style='font-size:14px; font-weight:600; color:#333; margin-bottom:8px;'>이메일 주소</div>", unsafe_allow_html=True)
st.text_input("email_input", label_visibility="collapsed", placeholder="example@nextwave.com")
st.markdown("<div style='font-size:11px; color:#888; margin-top:5px;'>※ 별도의 인증 없이 즉시 시작 가능합니다.</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # 폰 화면 끝

st.markdown('</div>', unsafe_allow_html=True) # 폰 베젤 끝

# --- 담당자 설득을 위한 사이드바 설명 ---
st.sidebar.title("📱 Test 1 실험군(B) 모바일 UI")
st.sidebar.markdown(f"""
이 퍼널 단계의 <span style='color:#d9534f; font-weight:bold;'>최종 이탈률 71.9%</span>를 방어하기 위한 모바일 최적화 UI안입니다.

**설계 포인트:**
1. **프로그레스 바:** '가입이 거의 끝나간다'는 심리적 안도감 제공 (85% 시각화)
2. **소셜 로그인 최상단 배치:** 인증 단계를 생략하여 즉시 가입 유도
3. **마이크로 카피:** '10초', '커피 한 모금' 등 시간 단축 메시지로 인지적 저항 최소화
""", unsafe_allow_html=True)
