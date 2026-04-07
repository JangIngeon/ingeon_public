import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="NextWave A/B Test Prototype", layout="wide")

st.title("🧪 NextWave 마케팅 캠페인 A/B 테스트 프로토타입")
st.markdown("---")

# 사이드바: 테스트 선택
test_selection = st.sidebar.selectbox(
    "검증할 테스트 설계안을 선택하세요",
    ["1. 가입 프로세스 최적화", "2. 요금제 섹션 가치 제안", "3. 직장인 맞춤형 소재"]
)

if test_selection == "1. 가입 프로세스 최적화":
    st.header("5.1. 가입 프로세스 최적화 및 심리적 허들 완화 테스트")
    st.info("핵심 지표: 가입 완료율 (목표 45% 이상)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("A안 (기존 다단계 폼)")
        st.caption("진행 상태 표시 없음 / 모든 정보 직접 입력")
        with st.form("form_a"):
            st.text_input("아이디(이메일)")
            st.text_input("비밀번호", type="password")
            st.text_input("비밀번호 확인", type="password")
            st.text_input("휴대폰 번호")
            st.button("본인인증 하기")
            st.form_submit_button("가입 완료")

    with col2:
        st.subheader("B안 (개선 - 간편 가입 & 보상 메시지)")
        st.caption("프로그레스 바 생성 / 심리적 보상 메시지 삽입")
        
        # 프로그레스 바 시각화
        st.write("📈 가입 완료까지 단 1분!")
        st.progress(70) # 70% 진행 상태 표시
        
        st.success("거의 다 됐습니다! 1분이면 생산성이 바뀝니다. ✨")
        
        st.button("🚀 Google로 3초 만에 시작하기", use_container_width=True)
        st.button("💬 Kakao로 간편 가입하기", use_container_width=True)
        
        with st.expander("이메일로 가입하기"):
            st.text_input("이메일 주소")
            st.button("가입 완료")
        
        st.markdown("> *지금 가입하고 직장인 78%가 경험한 업무 단축 효과를 누리세요.*")

elif test_selection == "2. 요금제 섹션 가치 제안":
    st.header("5.2. 요금제 섹션 이탈 방지 및 가치 강조 테스트")
    st.info("핵심 지표: 요금제 페이지 이탈률 (목표 35% 이하)")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("A안 (기존 나열식)")
        st.table(pd.DataFrame({
            "기능": ["일정 관리", "협업 메모", "업무 알림"],
            "Basic": ["O", "X", "X"],
            "Pro": ["O", "O", "O"]
        }))
        st.button("Pro 플랜 결제하기 (월 9,900원)")

    with col2:
        st.subheader("B안 (개선 - 무료 체험 & 성과 강조)")
        st.metric(label="직장인 평균 업무 시간 단축", value="20%", delta="NextWave 도입 후")
        st.write("---")
        st.write("✅ Pro 플랜의 모든 기능을 미리 경험해 보세요.")
        st.button("🎁 7일 무료 체험 후 결정하기", type="primary", use_container_width=True)
        st.caption("체험 기간 종료 24시간 전 알림을 드립니다. 위약금 제로!")

elif test_selection == "3. 직장인 맞춤형 소재":
    st.header("5.3. 핵심 타겟(직장인) 맞춤형 광고 소재 테스트")
    st.info("핵심 지표: SNS 가입 전환율 (목표 6% 이상)")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("A안 (기존 소재)")
        st.image("https://via.placeholder.com/400x200.png?text=NextWave:+Faster+Work", caption="범용 소재")
        st.write("문구: 업무를 더 빠르게 끝내세요. 당신의 하루를 정리하는 가장 쉬운 방법.")

    with col2:
        st.subheader("B안 (개선 - 직장인 공감형)")
        st.image("https://via.placeholder.com/400x200.png?text=NextWave:+Go+Home+Early", caption="직장인 타겟 특화")
        st.write("**문구:** 👨‍💻 나만 알고 싶은 칼퇴 치트키, 옆자리 김대리도 몰래 쓰기 시작함.")
        st.write("**버튼:** 지금 바로 업무 자동화하기")
