import streamlit as st

# 페이지 설정
st.set_page_config(page_title="NextWave UI Strategy Mockup", layout="wide")

# CSS: PC 배경과 스마트폰 프레임, 그리고 기획 문구 스타일링
st.markdown("""
    <style>
    /* 전체 배경: 세련된 다크 그레이 */
    .stApp {
        background-color: #f0f2f6;
    }

    /* 메인 컨테이너 레이아웃 */
    .main-container {
        display: flex;
        justify-content: space-around;
        align-items: flex-start;
        padding: 50px;
        gap: 50px;
    }

    /* 왼쪽: 기획 전략 카드 (PC 화면 느낌) */
    .strategy-card {
        flex: 1;
        background: white;
        padding: 40px;
        border-radius: 20px;
        border-left: 8px solid #1a4a7c;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* 오른쪽: 스마트폰 프레임 */
    .phone-mockup {
        width: 360px;
        height: 740px;
        background: #111;
        border-radius: 50px;
        padding: 12px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.3);
        position: relative;
        border: 4px solid #444;
    }

    .phone-screen {
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 38px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        font-family: 'Pretendard', sans-serif;
    }

    /* 스마트폰 내부 UI 요소 */
    .status-bar { padding: 15px 25px 5px; display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; }
    .progress-bar-container { padding: 20px 25px 10px; }
    .progress-text { font-size: 11px; color: #1a4a7c; font-weight: bold; margin-bottom: 5px; display: block; }
    
    .ui-content { padding: 30px 25px; text-align: center; }
    .main-copy { font-size: 22px; font-weight: 800; color: #1a4a7c; line-height: 1.4; margin-bottom: 12px; }
    .sub-copy { font-size: 13px; color: #666; line-height: 1.5; margin-bottom: 35px; }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%; height: 55px; border-radius: 12px; font-weight: bold; border: none; margin-bottom: 12px;
    }
    .kakao-btn button { background-color: #FEE500 !important; color: #3c1e1e !important; }
    .google-btn button { background-color: white !important; color: #333 !important; border: 1px solid #ddd !important; }

    /* 하이라이트 효과 */
    .highlight { background-color: #fff3cd; font-weight: bold; padding: 2px 5px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# 화면 구성
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="strategy-card">
        <h2 style='color: #1a4a7c; margin-bottom: 25px;'>📋 Test 1. UI 설계 전략</h2>
        <p style='font-size: 18px; line-height: 1.8; color: #444;'>
            "현재 가입 프로세스의 복잡도를 해결하기 위해 
            <span class="highlight">가입 절차를 최대한 간소화</span>한 방식을 적용한다.<br><br>
            <span class="highlight">구글·카카오 소셜 로그인 버튼을 최상단에 배치</span>하고, 
            실시간 <span class="highlight">프로그레스 바로 잔여 단계</span>를 직관적으로 제시하며,<br><br>
            <b>'커피 한 모금 마시는 사이 가입 끝. 당신의 소중한 시간을 10초도 뺏지 않겠습니다.'</b>라는 문구로 인지적 저항을 낮춘다."
        </p>
        <hr style='margin: 30px 0;'>
        <p style='font-size: 14px; color: #888;'>
            * 데이터 근거: 가입 단계 최종 이탈률 71.9% 방어 목적 [cite: 88, 34]
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # 스마트폰 프레임 시작
    st.markdown("""
    <div class="phone-mockup">
        <div class="phone-screen">
            <div class="status-bar">
                <span>9:41</span>
                <span>📶 🔋</span>
            </div>
    """, unsafe_allow_html=True)
    
    # 내부 UI 구현
    st.markdown('<div class="progress-bar-container">', unsafe_allow_html=True)
    st.markdown('<span class="progress-text">가입 완료까지 단 10초 남았습니다! (85%)</span>', unsafe_allow_html=True)
    st.progress(85)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ui-content">
        <div class="main-copy">커피 한 모금 마시는 사이<br>가입 끝! ☕</div>
        <div class="sub-copy">당신의 소중한 시간을<br>10초도 뺏지 않겠습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 영역
    col_k, col_g = st.columns(1)
    with col_k:
        st.markdown('<div class="kakao-btn">', unsafe_allow_html=True)
        if st.button("🟡 카카오로 1초 만에 시작하기"):
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_g:
        st.markdown('<div class="google-btn">', unsafe_allow_html=True)
        st.button("⚪ 구글로 계속하기")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
            <div style="text-align:center; color:#bbb; font-size:12px; margin-top:15px;">또는</div>
            <div style="padding: 20px 25px;">
                <div style="font-size:12px; color:#333; margin-bottom:5px;">이메일 주소</div>
                <div style="background:#f4f4f4; height:45px; border-radius:8px; border:1px solid #eee; padding:12px; color:#aaa; font-size:13px;">
                    example@nextwave.com
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 실행 가이드
st.sidebar.title("시연 가이드")
st.sidebar.info("""
1. 왼쪽 카드: 기획서의 핵심 전략 텍스트입니다. 
2. 오른쪽 스마트폰: 해당 전략이 실제 UI로 구현된 모습입니다.
3. 카카오 버튼을 클릭하면 실제 가입이 완료되는 듯한 상호작용(풍선)이 발생합니다.
""")
