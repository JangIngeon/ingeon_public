import streamlit as st

st.set_page_config(page_title="NextWave UI 개선안", layout="wide")

# UI 스타일 설정
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .control-box { border: 2px solid #dee2e6; padding: 20px; border-radius: 10px; background: white; min-height: 450px; }
    .test-box { border: 2px solid #1a4a7c; padding: 20px; border-radius: 10px; background: white; min-height: 450px; box-shadow: 0 4px 12px rgba(26,74,124,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 UI/UX 실험안 시각화")
st.caption("텍스트 위주의 설계서를 실제 화면 구현체로 확인하는 페이지입니다.")

tabs = st.tabs(["Test 1. 가입 프로세스", "Test 2. 메인 메시지", "Test 3. 요금제/제휴"])

# --- Test 1. 가입 프로세스 (하단 퍼널) ---
with tabs[0]:
    st.subheader("가입 완료율 개선을 위한 인증 절차 간소화")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="control-box">', unsafe_allow_html=True)
        st.info("기존: 5단계 정보 입력")
        st.text_input("이메일", placeholder="example@nextwave.com")
        st.text_input("비밀번호", type="password")
        st.text_input("이름")
        st.text_input("소속")
        st.button("이메일 인증코드 발송")
        st.caption("※ 이메일 인증 완료 후 가입이 승인됩니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="test-box">', unsafe_allow_html=True)
        st.success("개선: 소셜 가입 & 프로그레스 바")
        st.progress(80, text="가입 완료까지 10초 남았습니다 (80%)") [cite: 86]
        st.button("🟡 카카오로 1초 만에 시작하기") [cite: 88]
        st.button("⚪ 구글로 시작하기") [cite: 88]
        st.divider()
        st.markdown("<center><b>'커피 한 모금 마시는 사이 가입 끝!'</b></center>", unsafe_allow_html=True) [cite: 88]
        st.caption("당신의 소중한 시간을 10초도 뺏지 않겠습니다.") [cite: 88]
        st.markdown('</div>', unsafe_allow_html=True)

# --- Test 2. 메인 메시지 (중단 퍼널) ---
with tabs[1]:
    st.subheader("초기 직장인 타겟 맞춤형 마이크로 카피")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="control-box">', unsafe_allow_html=True)
        st.info("기존: 기능 중심")
        st.header("업무를 더 빠르게 끝내세요") [cite: 97]
        st.write("일정 관리, 협업 메모, 알림 기능을 제공합니다.")
        st.button("서비스 시작하기")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="test-box">', unsafe_allow_html=True)
        st.success("개선: 페인 포인트 공략")
        st.header("사수 도움 없이도 칭찬받는 '실무 치트키'") [cite: 97]
        st.write("✅ 신입 사원 1,400명이 이미 업무 시간을 절반으로 줄였습니다.") [cite: 97]
        st.warning("🎁 지금 가입 시 '주니어 전용 템플릿 패키지' 즉시 증정")
        st.button("무료로 치트키 템플릿 받기") [cite: 97]
        st.markdown('</div>', unsafe_allow_html=True)

# --- Test 3. 요금제/제휴 (상단 퍼널) ---
with tabs[2]:
    st.subheader("제휴사 유입 고객용 심리적 허들 제거")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="control-box">', unsafe_allow_html=True)
        st.info("기존: 정적 요금제 노출")
        st.write("### 월 9,900원") [cite: 108]
        st.write("- 모든 기능 무제한")
        st.write("- 팀 협업 툴 포함")
        st.button("카드 등록하고 시작하기")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="test-box">', unsafe_allow_html=True)
        st.success("개선: 혜택 강조 및 가격 상쇄")
        st.write("### 0원 (14일 무료 체험)") [cite: 109]
        st.write("✅ **카드 등록 없이 바로 시작하세요**") [cite: 109]
        st.write("☕ 커피 2잔 가격으로 얻는 매일 1시간의 여유") [cite: 110]
        st.markdown("**[제휴사 추천 전용] 실무 템플릿 패키지 포함**") [cite: 109]
        st.button("부담 없이 체험 시작하기")
        st.markdown('</div>', unsafe_allow_html=True)
