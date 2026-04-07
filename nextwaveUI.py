import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="NextWave 회원가입", layout="centered")

# 사용자 정의 CSS (블록형 프로그레스 바 및 디자인 개선)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* 블록형 프로그레스 바 스타일 */
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    .progress-block {
        height: 12px;
        flex: 1;
        margin-right: 5px;
        border-radius: 2px;
        background-color: #e9ecef;
    }
    .progress-block.active {
        background-color: #0056b3;
    }
    .progress-text {
        text-align: right;
        font-size: 0.85em;
        color: #0056b3;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .message-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .highlight { color: #0056b3; font-weight: bold; }
    .stButton > button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 1. 블록형 프로그레스 바 및 퍼센트 표시
# 현재 3단계 중 2단계 진행 중으로 가정 (75%)
st.write("### 가입 완료까지 단 **1분**!")
st.markdown("""
    <div class="progress-container">
        <div class="progress-block active"></div>
        <div class="progress-block active"></div>
        <div class="progress-block active"></div>
        <div class="progress-block"></div>
    </div>
    <div class="progress-text">현재 단계: 75% 완료</div>
    """, unsafe_allow_html=True)

# 2. 직장인 타겟 핵심 메시지 (전략 1 & 3 반영)
st.markdown(f"""
    <div class="message-box">
        <h4 style="margin-bottom: 10px;">"오늘부터 <span class="highlight">칼퇴</span>를 앞당기는 마지막 단계입니다."</h4>
        <p style="color: #666; font-size: 0.95em;">가입 즉시 <b>직장인 78%</b>가 만족한 실무 자동화 템플릿을 보내드려요.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. 가입/로그인 섹션 구분 (탭 활용)
tab1, tab2 = st.tabs(["⚡ 간편 소셜 시작", "📧 NextWave 계정"])

with tab1:
    st.write("")
    st.button("🚀 Google로 3초 만에 시작", key="google_btn")
    st.button("💬 Kakao로 간편 가입하기", key="kakao_btn")
    st.button("🟢 Naver로 3초 만에 시작", key="naver_btn")
    st.caption("클릭 한 번으로 가입 절차 없이 바로 시작할 수 있습니다.")

with tab2:
    st.write("")
    signup_mode = st.radio("선택해 주세요", ["기존 계정으로 로그인", "이메일로 신규 가입"], horizontal=True)
    
    with st.form("nextwave_form"):
        st.text_input("이메일 주소", placeholder="work@nextwave.com")
        st.text_input("비밀번호", type="password", placeholder="8자리 이상 입력")
        
        if signup_mode == "이메일로 신규 가입":
            st.text_input("비밀번호 확인", type="password")
            btn_label = "계정 생성 및 가입 완료"
        else:
            btn_label = "로그인 및 시작하기"
            
        st.info("💡 이미 수많은 실무자들이 NextWave로 업무를 자동화하고 있습니다.")
        
        submitted = st.form_submit_button(btn_label)
        if submitted:
            st.success("반갑습니다! NextWave와 함께 생산성을 높여보세요.")

# 4. 하단 푸터
st.markdown("<br><p style='text-align: center; font-size: 0.8em; color: #888;'>전 세계 10,000개 이상의 팀이 NextWave와 함께하고 있습니다.</p>", unsafe_allow_html=True)
