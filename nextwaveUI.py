import streamlit as st

# 모바일 앱 환경 설정
st.set_page_config(page_title="NextWave 가입 완료", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .app-header {
        text-align: center;
        padding: 15px;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border-radius: 0 0 12px 12px;
        margin-bottom: 20px;
    }
    /* 강조 박스 스타일 */
    .reward-box {
        background-color: #f0f7ff;
        border: 2px dashed #0056b3;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .highlight-blue { color: #0056b3; font-weight: bold; }
    
    /* 블록형 프로그레스 바 */
    .block-progress-container { display: flex; gap: 5px; margin: 15px 0; }
    .progress-unit { height: 8px; flex: 1; background: #eee; border-radius: 2px; }
    .progress-unit.filled { background: #0056b3; }
    
    .stButton > button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; font-size: 1.1em; }
    .secondary-btn > div > button { 
        background-color: white !important; 
        color: #666 !important; 
        border: 1px solid #ccc !important; 
        height: 40px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 상태 관리
if 'app_step' not in st.session_state:
    st.session_state.app_step = 3 # 3단계(회원가입)부터 시작하도록 설정

# 3단계: 회원가입 (71.9% 이탈 해결 집중 UI)
if st.session_state.app_step == 3:
    st.markdown('<div class="app-header">마지막 단계</div>', unsafe_allow_html=True)
    
    # 1. 블록형 프로그레스 바: "다 왔다"는 안도감 부여
    st.markdown('<div class="block-progress-container"><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit"></div></div><p style="text-align:right; font-size:0.8em; color:#0056b3; font-weight:bold;">지금 가입하면 75% 완료!</p>', unsafe_allow_html=True)

    # 2. 강력한 메시지와 템플릿 보상 강조 (전략적 핵심)
    st.markdown("""
        <div class="reward-box">
            <h4 style="margin-bottom: 10px;">"오늘부터 <span class="highlight-blue">칼퇴</span>를 시작하세요."</h4>
            <p style="font-size:0.9em; color:#444; line-height:1.5;">
                지금 가입 즉시 <span class="highlight-blue">직장인 78%</span>가 대만족한<br>
                <b>'실무 자동화 템플릿 5종'</b>을 메일로 보내드려요! 🎁
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3. 가입 절차 간소화: 소셜 로그인 전면 배치
    st.write("---")
    st.button("🚀 Google로 3초 만에 시작")
    st.button("💬 Kakao로 간편 시작")
    st.button("🟢 Naver로 간편 시작")
    
    st.markdown("<p style='text-align:center; color:#ccc; font-size:0.8em; margin:15px 0;'>또는 이메일로 가입하기</p>", unsafe_allow_html=True)

    # 4. 자체 계정 가입 및 로그인 (Tabs 활용)
    acc_tab1, acc_tab2 = st.tabs(["📧 신규 가입", "🔑 기존 로그인"])
    
    with acc_tab1:
        with st.form("signup_form"):
            st.text_input("업무용 이메일", placeholder="work@company.com")
            st.text_input("비밀번호", type="password", help="8자리 이상 입력")
            st.info("💡 이미 많은 동료들이 템플릿으로 업무를 단축하고 있습니다.")
            if st.form_submit_button("가입 완료하고 템플릿 받기"):
                st.session_state.app_step = 4
                st.rerun()

    with acc_tab2:
        with st.form("login_form"):
            st.text_input("이메일", placeholder="example@nextwave.com")
            st.text_input("비밀번호 ", type="password")
            if st.form_submit_button("로그인하기"):
                st.session_state.app_step = 4
                st.rerun()

    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("⬅ 요금제 다시 확인"):
        st.session_state.app_step = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 4단계: 가입 완료 (최종 보상 확인)
elif st.session_state.app_step == 4:
    st.balloons()
    st.markdown('<div class="app-header">Welcome!</div>', unsafe_allow_html=True)
    st.success("반갑습니다! 당신의 워크플로우가 이제 바뀝니다.")
    
    st.markdown("""
        <div style="text-align:center; padding: 20px;">
            <h3>🎉 가입 축하 선물 도착</h3>
            <p>입력하신 메일함에서 <b>'실무 자동화 템플릿'</b>을 확인하세요.</p>
            <p style="font-size:0.8em; color:#666;">(메일이 오지 않았다면 스팸함도 확인해 주세요!)</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("서비스 대시보드로 이동"):
        st.session_state.app_step = 1
        st.rerun()
