import streamlit as st

# 모바일 앱 환경 설정
st.set_page_config(page_title="NextWave Mobile", layout="centered")

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
    /* 요금제 카드 스타일 */
    .pricing-card {
        background: #fff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .pricing-card.best { border: 2px solid #0056b3; background-color: #f8fbff; }
    .plan-badge {
        display: inline-block;
        background: #0056b3;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7em;
        margin-bottom: 8px;
    }
    /* 블록형 프로그레스 바 */
    .block-progress-container { display: flex; gap: 5px; margin: 15px 0; }
    .progress-unit { height: 6px; flex: 1; background: #eee; border-radius: 2px; }
    .progress-unit.filled { background: #0056b3; }
    
    .stButton > button { width: 100%; border-radius: 8px; height: 48px; font-weight: 600; }
    /* 이전 버튼 스타일 */
    .secondary-btn > div > button { 
        background-color: white !important; 
        color: #666 !important; 
        border: 1px solid #ccc !important; 
        height: 40px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 상태 관리 (이전/다음 이동용)
if 'app_step' not in st.session_state:
    st.session_state.app_step = 1

# --- 단계별 화면 구현 ---

# 1단계: 서비스 소개 (랜딩)
if st.session_state.app_step == 1:
    st.markdown('<div class="app-header">NextWave</div>', unsafe_allow_html=True)
    st.title("일과 삶의 파도를 넘는 스마트한 방법")
    st.write("초기 직장인 가입자의 51.3%가 이미 경험 중입니다.")
    st.info("📌 **핵심 가치**\n- 업무 시간 20% 단축 증명\n- AI 일정 관리 및 실시간 협업")
    
    if st.button("내게 맞는 요금제 확인하기 ➔"):
        st.session_state.app_step = 2
        st.rerun()

# 2단계: 요금제 선택 (이탈률 45% 개선 전략)
elif st.session_state.app_step == 2:
    st.markdown('<div class="app-header">요금제 선택</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9em;'>지금 시작하면 <b>7일간 모든 기능을 무료</b>로 체험할 수 있습니다.</p>", unsafe_allow_html=True)

    # Free 플랜 (대학생 이탈 방지)
    st.markdown('<div class="pricing-card"><div class="plan-name"><b>Free (평생 무료)</b></div><div style="color:#0056b3; font-size:1.2em; font-weight:bold;">0원</div><div style="font-size:0.8em; color:#666;">개인용 일정 관리 및 메모</div></div>', unsafe_allow_html=True)

    # Starter Pro (직장인 타겟 핵심 플랜)
    st.markdown('<div class="pricing-card best"><div class="plan-badge">추천: 직장인 78% 선택</div><div class="plan-name"><b>Starter Pro (개인/프리랜서)</b></div><div style="color:#0056b3; font-size:1.2em; font-weight:bold;">4,900원 <small style="color:#999; font-weight:normal;">/월</small></div><div style="font-size:0.8em; color:#666;">• 실무 자동화 템플릿 제공<br>• 카드 등록 없이 무료 체험</div></div>', unsafe_allow_html=True)

    if st.button("Starter Pro 무료 체험 시작하기"):
        st.session_state.app_step = 3
        st.rerun()
    
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("⬅ 이전 페이지로"):
        st.session_state.app_step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3단계: 회원가입 (71.9% 이탈 해결 UI)
elif st.session_state.app_step == 3:
    st.markdown('<div class="app-header">회원가입</div>', unsafe_allow_html=True)
    
    # 블록형 프로그레스 바 (75% 지점)
    st.markdown('<div class="block-progress-container"><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit"></div></div><p style="text-align:right; font-size:0.75em; color:#0056b3; font-weight:bold;">마지막 단계: 75% 완료</p>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'><h4 style='color:#0056b3;'>오늘부터 칼퇴를 시작하세요.</h4><p style='font-size:0.8em; color:#666;'>1분이면 모든 준비가 끝납니다.</p></div>", unsafe_allow_html=True)

    # 간편 소셜 가입
    st.button("🚀 Google로 시작하기")
    st.button("💬 Kakao로 간편 가입하기")
    st.button("🟢 Naver로 시작하기")
    
    st.markdown("<p style='text-align:center; color:#ccc; font-size:0.8em; margin:10px 0;'>또는</p>", unsafe_allow_html=True)

    # 자체 계정 로그인 및 회원가입 섹션 (Tabs 활용)
    acc_tab1, acc_tab2 = st.tabs(["📧 이메일 가입", "🔑 기존 계정 로그인"])
    
    with acc_tab1:
        with st.form("signup_form"):
            st.text_input("업무용 이메일", placeholder="work@company.com")
            st.text_input("비밀번호", type="password")
            if st.form_submit_button("가입 완료 및 템플릿 받기"):
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

# 4단계: 완료
elif st.session_state.app_step == 4:
    st.balloons()
    st.markdown('<div class="app-header">가입 완료</div>', unsafe_allow_html=True)
    st.success("반갑습니다! 당신의 워크플로우가 이제 바뀝니다.")
    st.write("메일함으로 전송된 **'칼퇴 치트키 템플릿'**을 확인해 보세요.")
    
    if st.button("처음으로 돌아가기"):
        st.session_state.app_step = 1
        st.rerun()
