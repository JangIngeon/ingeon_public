import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="NextWave | 생산성 혁신", layout="centered")

# 사용자 정의 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .hero-section { text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #0056b3 0%, #003d80 100%); color: white; border-radius: 15px; margin-bottom: 40px; }
    .feature-card { background: white; padding: 25px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 20px; }
    .pricing-card { background: white; padding: 30px; border-radius: 12px; border: 2px solid #0056b3; text-align: center; }
    .highlight { color: #0056b3; font-weight: bold; }
    
    /* 블록형 프로그레스 바 */
    .progress-container { display: flex; justify-content: space-between; margin-bottom: 5px; }
    .progress-block { height: 12px; flex: 1; margin-right: 5px; border-radius: 2px; background-color: #e9ecef; }
    .progress-block.active { background-color: #0056b3; }
    .progress-text { text-align: right; font-size: 0.85em; color: #0056b3; font-weight: bold; margin-bottom: 20px; }
    
    .message-box { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #dee2e6; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태로 페이지 전환 관리
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- 1 & 2. 랜딩페이지 진입 및 서비스 소개 섹션 ---
if st.session_state.page == 'landing':
    st.markdown("""
        <div class="hero-section">
            <h1>NextWave</h1>
            <p style='font-size: 1.2em;'>일과 삶의 파도를 넘는 가장 스마트한 방법</p>
            <br>
            <p>직장인 78%가 경험한 업무 자동화의 시작</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🛠 주요 기능 소개")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='feature-card'><b>📅 일정 관리</b><br>업무 우선순위를 한눈에 파악하세요.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><b>📝 협업 메모</b><br>팀원과 실시간으로 아이디어를 공유하세요.</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='feature-card'><b>🔔 스마트 알림</b><br>중요한 마감 기한을 놓치지 마세요.</div>", unsafe_allow_html=True)
    
    if st.button("넥스트웨이브 요금제 확인하기 ➔", use_container_width=True, type="primary"):
        st.session_state.page = 'pricing'
        st.rerun()

# --- 3. 요금제 섹션 도달 (전략적 개선 반영) ---
elif st.session_state.page == 'pricing':
    st.write("### 💰 합리적인 플랜으로 칼퇴를 예약하세요")
    st.info("💡 모든 플랜은 결제 정보 입력 없이 '7일 무료 체험'으로 시작할 수 있습니다.") # 이탈 방지 장치
    
    st.markdown("""
        <div class='pricing-card'>
            <span style='background:#e7f3ff; color:#0056b3; padding:5px 10px; border-radius:20px; font-size:0.8em; font-weight:bold;'>가장 인기있는 플랜</span>
            <h2 style='margin:10px 0;'>Pro 플랜</h2>
            <p style='font-size:1.5em; font-weight:bold;'>월 9,900원</p>
            <ul style='text-align:left; display:inline-block; margin-bottom:20px;'>
                <li>모든 유료 템플릿 무제한 제공</li>
                <li>무제한 협업 팀 생성</li>
                <li><b>직장인 평균 업무 시간 20% 단축 증명</b></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 7일 무료 체험 신청하기 (1분 소요)", use_container_width=True, type="primary"):
        st.session_state.page = 'signup'
        st.rerun()
    st.caption("체험 기간 종료 24시간 전 알림을 드립니다. 위약금 걱정 없이 시작하세요.")

# --- 4 & 5. 회원가입 버튼 클릭 및 가입 완료 (블록형 UI 적용) ---
elif st.session_state.page == 'signup':
    st.write("### 🚀 가입 완료까지 단 **1분**!")
    st.markdown("""
        <div class="progress-container">
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block"></div>
        </div>
        <div class="progress-text">현재 단계: 75% 완료</div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="message-box">
            <h4 style="margin-bottom: 10px;">"오늘부터 <span class="highlight">칼퇴</span>를 앞당기는 마지막 단계입니다."</h4>
            <p style="color: #666; font-size: 0.95em;">가입 즉시 <b>직장인 78%</b>가 만족한 실무 자동화 템플릿을 보내드려요.</p>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⚡ 간편 소셜 시작", "📧 NextWave 계정"])
    with tab1:
        st.write("")
        st.button("🚀 Google로 3초 만에 시작")
        st.button("💬 Kakao로 간편 가입하기")
        st.button("🟢 Naver로 3초 만에 시작")
        st.caption("클릭 한 번으로 가입 절차 없이 바로 시작할 수 있습니다.")
    with tab2:
        st.write("")
        signup_mode = st.radio("선택해 주세요", ["기존 계정으로 로그인", "이메일로 신규 가입"], horizontal=True)
        with st.form("nextwave_form"):
            st.text_input("이메일 주소", placeholder="work@nextwave.com")
            st.text_input("비밀번호", type="password", placeholder="8자리 이상 입력")
            submitted = st.form_submit_button("가입 완료하고 생산성 높이기")
            if submitted:
                st.session_state.page = 'complete'
                st.rerun()

elif st.session_state.page == 'complete':
    st.balloons()
    st.success("🎉 가입이 완료되었습니다!")
    st.markdown("""
        <div style='text-align:center; padding:40px;'>
            <h2>반갑습니다, 프로 일잘러님!</h2>
            <p>지금 바로 메일함에서 <b>'실무 자동화 템플릿'</b>을 확인해 보세요.</p>
            <br>
            <button style='padding:10px 20px; background:#0056b3; color:white; border:none; border-radius:5px;'>서비스 대시보드로 이동</button>
        </div>
    """, unsafe_allow_html=True)
