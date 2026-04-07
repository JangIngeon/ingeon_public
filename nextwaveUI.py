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
    /* 최종 단계 강조 보상 박스 */
    .reward-box {
        background-color: #f0f7ff;
        border: 2px dashed #0056b3;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .highlight-blue { color: #0056b3; font-weight: bold; }
    
    /* 블록형 프로그레스 바 스타일 */
    .block-progress-container { display: flex; gap: 6px; margin: 15px 0; }
    .progress-unit { height: 8px; flex: 1; background: #eee; border-radius: 2px; }
    .progress-unit.filled { background: #0056b3; }
    
    /* 버튼 스타일 최적화 */
    .stButton > button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold; font-size: 1.05em; }
    .secondary-btn > div > button { 
        background-color: white !important; 
        color: #666 !important; 
        border: 1px solid #ccc !important; 
        height: 42px !important; 
    }
    
    /* 요금제 카드 스타일 */
    .pricing-card {
        background: #fff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }
    .pricing-card.best { border: 2px solid #0056b3; background-color: #f8fbff; }
    </style>
    """, unsafe_allow_html=True)

# 페이지 상태 관리 (1: 랜딩, 2: 요금제, 3: 가입, 4: 완료)
if 'app_step' not in st.session_state:
    st.session_state.app_step = 1

# --- 1단계: 서비스 소개 ---
if st.session_state.app_step == 1:
    st.markdown('<div class="app-header">NextWave</div>', unsafe_allow_html=True)
    st.title("일과 삶의 파도를 넘는 스마트한 방법")
    st.write("이미 **초기 직장인 가입자의 51.3%**가 경험하고 있습니다.")
    st.info("💡 **NextWave 핵심 가치**\n- 직장인 평균 업무 시간 20% 단축 증명\n- AI 일정 관리 및 실시간 팀 협업")
    
    if st.button("내게 맞는 요금제 확인하기 ➔"):
        st.session_state.app_step = 2
        st.rerun()

# --- 2단계: 요금제 선택 (이탈률 45% 개선 전략) ---
elif st.session_state.app_step == 2:
    st.markdown('<div class="app-header">요금제 선택</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9em;'>지금 시작하면 <b>7일간 모든 기능을 무료</b>로 체험합니다.</p>", unsafe_allow_html=True)

    # 1. Free 플랜 (대학생 이탈 방지)
    st.markdown('<div class="pricing-card"><b>Free (평생 무료)</b><br><span style="color:#0056b3; font-size:1.2em; font-weight:bold;">0원</span><br><small>개인용 일정 관리 및 메모 기능</small></div>', unsafe_allow_html=True)

    # 2. Starter Pro (핵심 타겟 직장인 플랜)
    st.markdown('<div class="pricing-card best"><span style="background:#0056b3; color:white; padding:2px 6px; border-radius:4px; font-size:0.7em;">추천: 직장인 78% 선택</span><br><b>Starter Pro (개인/프리랜서)</b><br><span style="color:#0056b3; font-size:1.2em; font-weight:bold;">4,900원 /월</span><br><small>• 실무 자동화 템플릿 즉시 제공<br>• 카드 등록 없이 무료 체험</small></div>', unsafe_allow_html=True)

    if st.button("Starter Pro 무료 체험 시작하기"):
        st.session_state.app_step = 3
        st.rerun()
    
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("⬅ 이전 페이지로"):
        st.session_state.app_step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3단계: 최종 가입 (71.9% 이탈 해결 집중 UI) ---
elif st.session_state.app_step == 3:
    st.markdown('<div class="app-header">마지막 단계</div>', unsafe_allow_html=True)
    
    # 블록형 프로그레스 바: 75% 완료 시각화
    st.markdown('<div class="block-progress-container"><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit filled"></div><div class="progress-unit"></div></div><p style="text-align:right; font-size:0.75em; color:#0056b3; font-weight:bold;">현재 75% 완료 - 거의 다 왔어요!</p>', unsafe_allow_html=True)

    # 강력한 혜택 강조 (Reward Box)
    st.markdown("""
        <div class="reward-box">
            <h4 style="margin-bottom: 8px;">"오늘부터 <span class="highlight-blue">칼퇴</span>를 시작하세요."</h4>
            <p style="font-size:0.85em; color:#444;">
                가입 즉시 <b>'실무 자동화 템플릿 5종'</b>을<br>
                메일로 즉시 발송해 드립니다! 🎁
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 간편 소셜 시작
    st.button("🚀 Google로 3초 만에 시작")
    st.button("💬 Kakao로 간편 시작")
    st.button("🟢 Naver로 간편 시작")
    
    st.markdown("<p style='text-align:center; color:#ccc; font-size:0.8em; margin:10px 0;'>또는</p>", unsafe_allow_html=True)

    # 자체 계정 가입 및 로그인 (Tabs)
    tab_signup, tab_login = st.tabs(["📧 이메일 가입", "🔑 기존 로그인"])
    
    with tab_signup:
        with st.form("signup_form"):
            st.text_input("업무용 이메일", placeholder="work@company.com")
            st.text_input("비밀번호", type="password")
            st.caption("8자리 이상 입력해 주세요.")
            if st.form_submit_button("가입 완료 및 템플릿 받기"):
                st.session_state.app_step = 4
                st.rerun()

    with tab_login:
        with st.form("login_form"):
            st.text_input("이메일 주소", placeholder="example@nextwave.com")
            st.text_input("비밀번호 ", type="password")
            if st.form_submit_button("로그인하기"):
                st.session_state.app_step = 4
                st.rerun()

    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("⬅ 요금제 다시 확인"):
        st.session_state.app_step = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4단계: 가입 완료 ---
elif st.session_state.app_step == 4:
    st.balloons()
    st.markdown('<div class="app-header">가입 완료</div>', unsafe_allow_html=True)
    st.success("반갑습니다! 당신의 워크플로우가 이제 바뀝니다.")
    
    st.markdown("""
        <div style="text-align:center; padding: 20px;">
            <h3>🎉 선물 도착</h3>
            <p>메일함에서 <b>'실무 자동화 템플릿'</b>을 확인하세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("처음으로 돌아가기"):
        st.session_state.app_step = 1
        st.rerun()
