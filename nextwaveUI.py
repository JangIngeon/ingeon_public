import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="NextWave 회원가입", layout="centered")

# 사용자 정의 CSS (디자인 개선)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stProgress > div > div > div > div { background-color: #0056b3; }
    .message-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        text-align: center;
        margin-bottom: 20px;
    }
    .highlight { color: #0056b3; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 1. 상단 프로그레스 바 및 소요 시간 안내
st.write("### 🚀 가입 완료까지 단 **1분**!")
st.progress(75)  # 75% 진행 상태 표시
st.caption("거의 다 됐습니다! 마지막 정보만 확인하면 끝납니다.")

st.markdown("---")

# 2. 직장인 타겟 핵심 메시지 섹션
st.markdown(f"""
    <div class="message-box">
        <h4>"오늘부터 <span class="highlight">칼퇴</span>를 앞당기는 마지막 단계입니다."</h4>
        <p style="color: #666; font-size: 0.9em;">가입 즉시 <b>직장인 78%</b>가 경험한 실무 템플릿 5종을 바로 보내드려요.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. 소셜 로그인 버튼 (가입 절차 간소화)
st.subheader("간편 가입하기")
col1, col2 = st.columns(2)
with col1:
    st.button("🚀 Google로 3초 만에 시작", use_container_width=True)
with col2:
    st.button("💬 Kakao로 3초 만에 시작", use_container_width=True)

st.markdown("<p style='text-align: center; color: #aaa;'>또는</p>", unsafe_allow_html=True)

# 4. 필수 정보 입력 폼 (항목 최소화)
with st.container():
    with st.form("signup_form"):
        st.text_input("이메일 주소", placeholder="work@nextwave.com")
        st.text_input("비밀번호", type="password", placeholder="8자리 이상 입력")
        
        # 가입 동기 부여 메시지
        st.info("💡 이미 수많은 실무자들이 넥스트웨이브로 업무를 자동화하고 있습니다.")
        
        # 최종 제출 버튼
        submitted = st.form_submit_button("가입 완료하고 생산성 높이기", use_container_width=True)
        
        if submitted:
            st.success("환영합니다! 이제 당신의 워크플로우가 바뀝니다.")

# 5. 하단 푸터 (신뢰 기반 사회적 증명)
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #888;'>전 세계 10,000개 이상의 팀이 넥스트웨이브와 함께하고 있습니다.</p>", unsafe_allow_html=True)
