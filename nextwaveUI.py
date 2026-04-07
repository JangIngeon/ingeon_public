import streamlit as st

# 모바일 앱 환경 설정
st.set_page_config(page_title="NextWave Mobile", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 */
    .stApp { background-color: #ffffff; }
    
    /* 상단 앱 바 */
    .app-header {
        text-align: center;
        padding: 15px;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 20px;
        border-radius: 0 0 12px 12px;
    }

    /* 모바일 최적화 요금제 카드 스타일 */
    .pricing-card {
        background: #fff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .pricing-card.best {
        border: 2px solid #0056b3;
        background-color: #f8fbff;
    }
    .plan-badge {
        display: inline-block;
        background: #0056b3;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7em;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .plan-name { font-size: 1em; font-weight: bold; color: #333; }
    .plan-price { font-size: 1.3em; font-weight: 800; color: #0056b3; margin: 4px 0; }
    .plan-desc { font-size: 0.85em; color: #666; line-height: 1.4; }

    /* 블록형 프로그레스 바 */
    .block-progress-container { display: flex; gap: 5px; margin: 15px 0; }
    .progress-unit { height: 6px; flex: 1; background: #eee; border-radius: 2px; }
    .progress-unit.filled { background: #0056b3; }
    .progress-label { text-align: right; font-size: 0.75em; color: #0056b3; font-weight: bold; }

    /* 모바일 버튼 최적화 */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 상태 관리
if 'app_page' not in st.session_state:
    st.session_state.app_page = 'intro'

# 1. 서비스 소개 단계 (랜딩 및 소개)
if st.session_state.app_page == 'intro':
    st.markdown('<div class="app-header">NextWave</div>', unsafe_allow_html=True)
    st.title("일과 삶의 파도를 넘는 스마트한 방법")
    st.write("초기 직장인 가입자의 51.3%가 이미 경험 중입니다.") # 타겟 데이터 반영
    
    st.info("📌 **주요 기능**\n- AI 일정 관리 & 협업 메모\n- 업무 시간 20% 단축 증명")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("내게 맞는 요금제 확인하기"):
        st.session_state.app_page = 'plans'
        st.rerun()

# 2. 요금제 섹션 (이탈률 45.0% 개선을 위한 다각화)
elif st.session_state.app_page == 'plans':
    st.markdown('<div class="app-header">요금제 선택</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9em; color:#555;'>지금 시작하면 <b>7일간 모든 기능을 무료</b>로 체험할 수 있습니다.</p>", unsafe_allow_html=True)

    # 1) Free 플랜: 대학생 팀플형 이탈 방지
    st.markdown("""
        <div class="pricing-card">
            <div class="plan-name">Free (평생 무료)</div>
            <div class="plan-price">0원</div>
            <div class="plan-desc">개인용 기본 일정 관리 및 메모 기능 제공</div>
        </div>
    """, unsafe_allow_html=True)

    # 2) Starter Pro: 초기 직장인 타겟 핵심 플랜
    st.markdown("""
        <div class="pricing-card best">
            <div class="plan-badge">인기: 직장인 78% 선택</div>
            <div class="plan-name">Starter Pro (개인/프리랜서)</div>
            <div class="plan-price">4,900원 <span style='font-size:0.6em; color:#999;'>/월</span></div>
            <div class="plan-desc">
                • <b>실무 자동화 템플릿</b> 무제한 제공<br>
                • <b>카드 등록 없이</b> 7일 무료 체험
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3) Team Biz: B2B 확장 전략 반영
    st.markdown("""
        <div class="pricing-card">
            <div class="plan-name">Team Biz (조직용)</div>
            <div class="plan-price">9,900원 <span style='font-size:0.6em; color:#999;'>/인당</span></div>
            <div class="plan-desc">팀 단위 권한 관리 및 통합 대시보드 제공</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Starter Pro 무료 체험 시작"):
        st.session_state.app_page = 'join'
        st.rerun()
    st.caption("체험 기간 종료 전 push 알림을 보내드립니다.")

# 3. 회원가입 단계 (71.9% 이탈 해결 UI)
elif st.session_state.app_page == 'join':
    st.markdown('<div class="app-header">회원가입</div>', unsafe_allow_html=True)
    
    # 블록형 프로그레스 바 (75% 지점)
    st.markdown("""
        <div class="block-progress-container">
            <div class="progress-unit filled"></div>
            <div class="progress-unit filled"></div>
            <div class="progress-unit filled"></div>
            <div class="progress-unit"></div>
        </div>
        <div class="progress-label">마지막 단계: 75% 완료</div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <h4 style='color:#0056b3; margin-bottom:5px;'>오늘부터 칼퇴를 시작하세요.</h4>
            <p style='font-size:0.8em; color:#666;'>1분이면 모든 준비가 끝납니다.</p>
        </div>
    """, unsafe_allow_html=True)

    # 간편 소셜 가입
    st.button("🚀 Google로 시작하기")
    st.button("💬 Kakao로 시작하기")
    st.button("🟢 Naver로 시작하기")
    
    st.markdown("<p style='text-align:center; color:#ccc; font-size:0.8em; margin:10px 0;'>또는</p>", unsafe_allow_html=True)

    # 자체 계정 폼
    with st.form("mobile_signup_form"):
        st.text_input("업무용 이메일", placeholder="work@company.com")
        st.text_input("비밀번호", type="password")
        if st.form_submit_button("가입 완료 및 템플릿 받기"):
            st.session_state.app_page = 'end'
            st.rerun()

# 4. 완료
elif st.session_state.app_page == 'end':
    st.balloons()
    st.markdown('<div class="app-header">Welcome!</div>', unsafe_allow_html=True)
    st.success("가입이 성공적으로 완료되었습니다!")
    st.write("메일함으로 전송된 **'칼퇴 치트키 템플릿'**을 지금 확인해 보세요.")
    if st.button("대시보드 시작하기"):
        st.session_state.app_page = 'intro'
        st.rerun()
