import streamlit as st

# 페이지 기본 설정 및 디자인
st.set_page_config(page_title="NextWave | 일과 삶의 파도를 넘는 스마트한 방법", layout="wide")

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .main { background-color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* 히어로 섹션 */
    .hero {
        text-align: center;
        padding: 80px 20px;
        background: linear-gradient(135deg, #0056b3 0%, #003d80 100%);
        color: white;
        border-radius: 0 0 50px 50px;
        margin-bottom: 50px;
    }
    
    /* 요금제 카드 공통 스타일 */
    .pricing-container {
        display: flex;
        justify-content: center;
        gap: 25px;
        padding: 20px;
        flex-wrap: wrap;
    }
    .price-card {
        background: white;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #e9ecef;
        width: 300px;
        text-align: center;
        transition: transform 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .price-card:hover { transform: translateY(-10px); border-color: #0056b3; }
    
    /* 직장인 제휴 플랜 강조 스타일 */
    .featured {
        border: 3px solid #0056b3;
        position: relative;
    }
    .badge {
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: #0056b3;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .price-title { font-size: 1.5em; font-weight: bold; margin-bottom: 10px; color: #333; }
    .price-val { font-size: 2.2em; font-weight: 800; color: #0056b3; margin-bottom: 20px; }
    .price-features { list-style: none; padding: 0; margin-bottom: 30px; text-align: left; }
    .price-features li { margin-bottom: 12px; color: #666; font-size: 0.95em; }
    .price-features li::before { content: "✓ "; color: #0056b3; font-weight: bold; }
    
    /* 블록형 프로그레스 바 */
    .progress-container { display: flex; justify-content: center; gap: 8px; margin-top: 30px; }
    .progress-block { height: 8px; width: 60px; border-radius: 4px; background-color: #e9ecef; }
    .progress-block.active { background-color: #0056b3; }
    
    .cta-button {
        display: inline-block;
        padding: 12px 30px;
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 세션 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 'landing'

# 1 & 2. 랜딩페이지 및 서비스 소개
if st.session_state.step == 'landing':
    st.markdown("""
        <div class="hero">
            <h1 style='font-size: 3.5em; margin-bottom: 20px;'>NextWave</h1>
            <p style='font-size: 1.3em; opacity: 0.9;'>일정관리, 협업메모, 스마트 알림을 하나로</p>
            <p style='font-size: 1.1em; font-weight: bold; margin-top: 20px;'>이미 초기 직장인 가입자의 51.3%가 생산성 혁신을 경험 중입니다</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.container()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📅 스마트 일정\n복잡한 업무 우선순위를 AI가 대신 정리합니다.")
    with col2:
        st.markdown("### 📝 실시간 협업\n소규모 팀을 위한 끊김 없는 메모 공유 시스템.")
    with col3:
        st.markdown("### 🔔 칼퇴 알림\n마감 기한 압박 없는 스마트한 업무 알림.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("지금 바로 나에게 맞는 요금제 찾기 ➔", type="primary", use_container_width=True):
        st.session_state.step = 'pricing'
        st.rerun()

# 3. 전략적 요금제 구성 (이탈률 최소화 설계)
elif st.session_state.step == 'pricing':
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>합리적인 선택으로 업무 효율을 높이세요</h2>", unsafe_allow_html=True)
    
    # 전략적 요금제 3종 구성
    st.markdown(f"""
        <div class="pricing-container">
            <div class="price-card">
                <div class="price-title">Free</div>
                <div class="price-val">0원 <small style='font-size: 0.4em; color: #999;'>/ 평생 무료</small></div>
                <ul class="price-features">
                    <li>개인 일정 관리 (기본)</li>
                    <li>협업 메모 3개 생성</li>
                    <li>기본 푸시 알림</li>
                    <li><b>대학생 팀플 최적화</b></li>
                </ul>
            </div>
            
            <div class="price-card featured">
                <div class="badge">직장인 78%가 선택한 플랜</div>
                <div class="price-title">Starter Pro</div>
                <div class="price-val">4,900원 <small style='font-size: 0.4em; color: #999;'>/ 월 (첫 달 무료)</small></div>
                <ul class="price-features">
                    <li><b>무제한</b> 협업 및 메모</li>
                    <li><b>칼퇴 치트키</b> 실무 템플릿 제공</li>
                    <li>전문가용 업무 자동화 알림</li>
                    <li><b>첫 7일 무료 체험 (결제X)</b></li>
                </ul>
            </div>
            
            <div class="price-card">
                <div class="price-title">Team Biz</div>
                <div class="price-val">9,900원 <small style='font-size: 0.4em; color: #999;'>/ 인당 월</small></div>
                <ul class="price-features">
                    <li>조직 단위 권한 관리</li>
                    <li>Bottom-up 협업 시스템</li>
                    <li>B2B 전용 기술 지원</li>
                    <li>대시보드 통합 관리</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Starter Pro 플랜**은 현재 SNS 광고 유입 유저에게만 제공되는 한정 제휴 혜택입니다.")
    
    if st.button("🚀 Starter Pro 무료 체험 시작하기 (1분 소요)", type="primary", use_container_width=True):
        st.session_state.step = 'signup'
        st.rerun()
    
    st.markdown("<p style='text-align: center; color: #999; margin-top: 10px;'>카드 정보 입력 없이 3초 만에 시작하세요.</p>", unsafe_allow_html=True)

# 4 & 5. 회원가입 프로세스 (UX 붕괴 방지 UI)
elif st.session_state.step == 'signup':
    st.markdown("<h2 style='text-align: center;'>거의 다 됐습니다! 딱 1분만 빌려주세요.</h2>", unsafe_allow_html=True)
    
    # 블록형 프로그레스 바
    st.markdown("""
        <div class="progress-container">
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block"></div>
        </div>
        <p style='text-align: center; color: #0056b3; font-weight: bold; margin-top: 10px;'>진행도: 75% (마지막 단계)</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ⚡ 소셜 로그인으로 3초 만에 완료")
        st.button("🚀 Google로 시작하기", use_container_width=True)
        st.button("💬 Kakao로 시작하기", use_container_width=True)
        st.button("🟢 Naver로 시작하기", use_container_width=True)
    
    with col2:
        st.markdown("### 📧 NextWave 자체 계정")
        with st.form("signup_form"):
            st.text_input("업무용 이메일", placeholder="work@company.com")
            st.text_input("비밀번호", type="password")
            if st.form_submit_button("가입 완료 및 템플릿 받기"):
                st.session_state.step = 'complete'
                st.rerun()

    st.success("💡 지금 가입하시면 **'옆자리 김대리도 몰래 쓰는 업무 자동화 템플릿'**을 즉시 메일로 발송해 드립니다.")

# 가입 완료
elif st.session_state.step == 'complete':
    st.balloons()
    st.markdown("""
        <div style='text-align: center; padding: 100px 20px;'>
            <h1 style='color: #0056b3;'>🎉 가입을 환영합니다!</h1>
            <p style='font-size: 1.5em; margin: 20px 0;'>오늘부터 당신의 퇴근 시간이 20% 빨라집니다.</p>
            <p>입력하신 이메일로 <b>무료 체험 가이드</b>와 <b>실무 템플릿</b>을 전송했습니다.</p>
            <br><br>
            <a href='#' style='padding: 15px 40px; background: #0056b3; color: white; border-radius: 8px; text-decoration: none; font-weight: bold;'>서비스 대시보드로 이동</a>
        </div>
    """, unsafe_allow_html=True)
