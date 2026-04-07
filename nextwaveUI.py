import streamlit as st

# 모바일 앱 스타일 설정
st.set_page_config(page_title="NextWave App", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 */
    .stApp { background-color: #ffffff; }
    
    /* 상단 앱 바 스타일 */
    .app-bar {
        text-align: center;
        padding: 15px;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 20px;
        border-radius: 0 0 15px 15px;
    }

    /* 모바일 전용 요금제 카드 스타일 (세로 나열 최적화) */
    .mobile-card {
        background: #fff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .mobile-card.featured {
        border: 2px solid #0056b3;
        background-color: #f8fbff;
    }
    .badge {
        display: inline-block;
        background: #0056b3;
        color: white;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.75em;
        margin-bottom: 10px;
    }
    .card-title { font-size: 1.1em; font-weight: bold; color: #333; }
    .card-price { font-size: 1.4em; font-weight: 800; color: #0056b3; margin: 5px 0; }
    .card-features { font-size: 0.9em; color: #666; margin-top: 10px; line-height: 1.5; }

    /* 블록형 프로그레스 바 */
    .progress-container { display: flex; gap: 4px; margin: 15px 0; }
    .progress-block { height: 6px; flex: 1; background: #e9ecef; border-radius: 2px; }
    .progress-block.active { background: #0056b3; }
    
    /* 버튼 스타일 커스텀 */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 'landing'

# 1. 랜딩 페이지 (서비스 소개)
if st.session_state.step == 'landing':
    st.markdown('<div class="app-bar">NextWave</div>', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/600x300.png?text=Smart+Productivity+for+Work", use_container_width=True)
    
    st.title("일과 삶의 파도를 넘는 방법")
    st.write("직장인 78%가 경험한 업무 자동화 솔루션 [cite: 154]")
    
    with st.expander("✨ 주요 기능 보기"):
        st.write("- **AI 일정 관리**: 우선순위 자동 배정 [cite: 96]")
        st.write("- **협업 메모**: 팀원과 실시간 공유 [cite: 98]")
        st.write("- **스마트 알림**: 칼퇴를 부르는 마감 관리 [cite: 154]")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("내게 맞는 플랜 찾기"):
        st.session_state.step = 'pricing'
        st.rerun()

# 2. 요금제 페이지 (이탈률 최소화 전략 반영) [cite: 91, 112]
elif st.session_state.step == 'pricing':
    st.markdown('<div class="app-bar">요금제 선택</div>', unsafe_allow_html=True)
    st.info("💡 모든 유료 플랜은 **7일 무료 체험**이 가능합니다. (결제 정보 불필요) [cite: 91]")

    # 무료 플랜 (이탈 방지용) [cite: 162]
    st.markdown("""
        <div class="mobile-card">
            <div class="card-title">Free (평생 무료)</div>
            <div class="card-price">0원</div>
            <div class="card-features">
                • 개인 일정 관리 기본<br>
                • 대학생 팀플 최적화 도구 [cite: 99]
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 직장인 타겟 제휴 플랜 (핵심 전략) [cite: 158]
    st.markdown("""
        <div class="mobile-card featured">
            <div class="badge">추천: 직장인 51.3% 선택 [cite: 96]</div>
            <div class="card-title">Starter Pro (제휴 혜택)</div>
            <div class="card-price">4,900원 <span style='font-size:0.6em; color:#999;'>/월</span></div>
            <div class="card-features">
                • <b>무제한</b> 협업 및 자동화<br>
                • <b>실무 자동화 템플릿</b> 즉시 제공 [cite: 159]<br>
                • 첫 달 무료 체험 가능
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 기업형 플랜 
    st.markdown("""
        <div class="mobile-card">
            <div class="card-title">Team Biz</div>
            <div class="card-price">9,900원 <span style='font-size:0.6em; color:#999;'>/인당</span></div>
            <div class="card-features">
                • 조직 단위 권한 및 보안<br>
                • B2B 전용 통합 대시보드 
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Starter Pro 무료 체험 시작"):
        st.session_state.step = 'signup'
        st.rerun()
    st.caption("체험 종료 전 알림을 드립니다. 위약금 걱정 없이 시작하세요. [cite: 91]")

# 3. 회원가입 페이지 (UX 병목 해소) 
elif st.session_state.step == 'signup':
    st.markdown('<div class="app-bar">회원가입</div>', unsafe_allow_html=True)
    
    # 블록형 프로그레스 바 (75% 지점 표시)
    st.markdown("""
        <div class="progress-container">
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block active"></div>
            <div class="progress-block"></div>
        </div>
        <p style='text-align:right; font-size:0.8em; color:#0056b3; font-weight:bold;'>마지막 단계 (75%)</p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <h4 style='color:#0056b3;'>"오늘부터 <b>칼퇴</b>하세요." [cite: 186]</h4>
            <p style='font-size:0.85em; color:#666;'>1분 만에 가입하고 실무 템플릿을 받으세요.</p>
        </div>
    """, unsafe_allow_html=True)

    # 소셜 가입 버튼 (이탈 방지 핵심) [cite: 204]
    st.button("🚀 Google로 시작하기")
    st.button("💬 Kakao로 시작하기")
    st.button("🟢 Naver로 시작하기")
    
    st.markdown("<p style='text-align:center; color:#ccc; margin:10px 0;'>또는</p>", unsafe_allow_html=True)

    with st.form("signup_form"):
        st.text_input("업무용 이메일", placeholder="work@company.com")
        st.text_input("비밀번호", type="password")
        if st.form_submit_button("가입 완료 및 혜택 받기"):
            st.session_state.step = 'complete'
            st.rerun()

# 4. 완료 페이지
elif st.session_state.step == 'complete':
    st.balloons()
    st.markdown('<div class="app-bar">가입 완료</div>', unsafe_allow_html=True)
    st.success("반갑습니다! 당신의 워크플로우가 이제 바뀝니다.")
    st.write("메일함으로 보낸 **'실무 템플릿'**을 지금 확인해 보세요. [cite: 159]")
    if st.button("홈으로 이동"):
        st.session_state.step = 'landing'
        st.rerun()
