import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------------------------------------------------
# 1. 페이지 설정 및 공통 함수
# ---------------------------------------------------------
st.set_page_config(page_title="배합고무 AI 품질 관제 시스템", layout="wide")

# 세션 상태 초기화 (가상 데이터 저장용)
if 'history' not in st.session_state:
    # 대시보드용 가상 과거 데이터 생성
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=10),
        'Batch_ID': [f'BATCH-{i:03d}' for i in range(10)],
        'Prediction': np.random.choice(['Pass', 'Fail'], 10, p=[0.8, 0.2]),
        'Actual': np.random.choice(['Pass', 'Fail'], 10, p=[0.85, 0.15])
    }
    st.session_state.history = pd.DataFrame(data)

# 레오커브 시뮬레이션 함수 (가상 데이터 생성)
def plot_rheo_curve(temp, time_mix):
    t = np.linspace(0, time_mix, 100)
    # 온도가 높으면 경화 속도가 빠름 (가상의 물리 식)
    torque = (np.log(t + 1) * (temp / 50)) + np.random.normal(0, 0.05, 100)
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(t, torque, label='Torque (dNm)', color='#1f77b4', linewidth=2)
    
    # 적정 가황 범위(가상 기준) 표시
    ax.axhspan(2.5, 3.5, color='green', alpha=0.1, label='Target Quality Range')
    
    ax.set_title(f"Real-time Rheometer Simulation ({temp}°C / {time_mix}min)")
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Torque (dNm)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig

# ---------------------------------------------------------
# 2. 사이드바 (시스템 상태)
# ---------------------------------------------------------
st.sidebar.title("🏭 Smart Factory")
st.sidebar.info("접속자: 인턴 (품질관리팀)")
st.sidebar.markdown("---")
st.sidebar.write("**시스템 상태**")
st.sidebar.success("🟢 AI 모델 서버: 정상")
st.sidebar.success("🟢 데이터베이스: 연결됨")

# ---------------------------------------------------------
# 3. 메인 화면 구성 (탭 구조)
# ---------------------------------------------------------
st.title("🌉 교량받침 배합고무 최적공정 솔루션")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. 공정 조건 검색 (작업 전)", 
    "📈 2. 실시간 모니터링 (작업 중)", 
    "📝 3. 데이터 입력 (작업 후)",
    "📊 4. 품질 분석 대시보드"
])

# --- [Tab 1] 작업 전 모델 공정 조건 검색 화면 ---
with tab1:
    st.header("1. 최적 공정 조건 검색 (AI Recommendation)")
    st.markdown("생산할 제품의 **목표 물성**을 입력하면 AI가 최적의 온도와 시간을 추천합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        target_hardness = st.number_input("목표 경도 (Hardness, Shore A)", 50, 80, 60)
    with col2:
        target_tensile = st.number_input("목표 인장강도 (Tensile Strength, MPa)", 10, 30, 20)
    
    if st.button("AI 최적 조건 검색"):
        with st.spinner("AI가 과거 데이터를 분석 중입니다..."):
            time.sleep(1) # 연출용 딜레이
            # 가상의 추천 로직
            rec_temp = 150 + (target_hardness - 60)
            rec_time = 15 + (target_tensile - 20)
            
            st.success("✅ 추천 공정 조건이 도출되었습니다.")
            st.metric(label="추천 가황 온도", value=f"{rec_temp} °C")
            st.metric(label="추천 배합 시간", value=f"{rec_time} 분")

# --- [Tab 2] 시각적 인터페이스 및 의사결정 지원 ---
with tab2:
    st.header("2. 실시간 배합 모니터링 & AI 판정")
    st.markdown("현장 작업자가 공정 진행 상황을 시각적으로 확인하고 의사결정합니다.")
    
    # 입력 시뮬레이션
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 현재 설비 세팅")
        curr_temp = st.slider("현재 온도 (°C)", 100, 200, 155)
        curr_time = st.slider("현재 시간 (분)", 5, 30, 18)
        
        # [안전성 정보 제공] 과열 경고 기능
        if curr_temp >= 180:
            st.error("⚠️ [WARNING] 과열 위험! 온도를 낮추세요.")
        else:
            st.info("✅ 안전 범위 내 작동 중")

        # AI 예측 결과
        st.markdown("---")
        st.subheader("🤖 AI 품질 예측")
        # 간단한 예측 로직 (가상)
        predicted_torque = np.log(curr_time + 1) * (curr_temp / 50)
        
        if 2.5 <= predicted_torque <= 3.5:
            st.markdown("## 🟢 적합 (PASS)")
            st.markdown("작업을 계속 진행하십시오.")
        else:
            st.markdown("## 🔴 부적합 (FAIL)")
            st.markdown("**즉시 공정 조건을 수정하십시오.**")

    with col2:
        st.subheader("📈 실시간 레오커브 (Rheo-curve)")
        fig = plot_rheo_curve(curr_temp, curr_time)
        st.pyplot(fig)

# --- [Tab 3] 수집 데이터 입력 화면 ---
with tab3:
    st.header("3. 작업 후 실측 데이터 입력")
    st.markdown("작업 완료 후 품질 검사 결과와 레오커브 이미지를 업로드합니다.")
    
    with st.form("input_form"):
        c1, c2 = st.columns(2)
        with c1:
            batch_id = st.text_input("배치 번호 (Batch ID)", "BATCH-2024-001")
            measured_hard = st.number_input("실측 경도", 0.0, 100.0)
        with c2:
            final_result = st.selectbox("최종 판정 결과", ["Pass", "Fail"])
            # [레오커브 이미지 입력 화면]
            uploaded_file = st.file_uploader("레오커브 이미지 업로드", type=['png', 'jpg'])
        
        submit = st.form_submit_button("데이터 저장")
        
        if submit:
            st.success(f"{batch_id} 데이터가 DB에 저장되었습니다.")
            # 세션 스테이트에 더미 데이터 추가 (대시보드 반영용)
            new_row = {
                'Date': pd.Timestamp.now(),
                'Batch_ID': batch_id,
                'Prediction': 'Pass', # 가정
                'Actual': final_result
            }
            # DataFrame 연결 (concat 사용)
            st.session_state.history = pd.concat([
                st.session_state.history, 
                pd.DataFrame([new_row])
            ], ignore_index=True)

# --- [Tab 4] 모델 예측 적중률 비교 대시보드 ---
with tab4:
    st.header("4. 품질 분석 & 모델 성능 대시보드")
    
    df = st.session_state.history
    
    # 적중률 계산
    df['Correct'] = df['Prediction'] == df['Actual']
    accuracy = df['Correct'].mean() * 100
    
    # KPI 지표 표시
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("총 생산 배치", f"{len(df)} 건")
    kpi2.metric("AI 모델 적중률", f"{accuracy:.1f}%", "1.2%")
    kpi3.metric("최근 불량률", "15.0%", "-2.5%")
    
    # 차트 영역
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 예측 vs 실측 일치 현황")
        # 막대 그래프
        match_counts = df['Correct'].value_counts().rename({True: 'Match', False: 'Mismatch'})
        st.bar_chart(match_counts)
        
    with c2:
        st.subheader("📉 최근 데이터 로그")
        st.dataframe(df.tail(5), use_container_width=True)
