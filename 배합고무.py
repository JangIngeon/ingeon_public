import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 화면 구성 (대시보드 타이틀)
st.title("🏭 배합 고무 품질 모니터링 시스템")
st.markdown("작업자 의사결정 지원을 위한 품질 예측 및 시각화")

# 2. 사이드바: 현장 작업자 입력 화면 구현
st.sidebar.header("1. 공정 조건 입력 (작업 전)")
temp = st.sidebar.slider("가열 온도 (°C)", 100, 200, 150)
time_mix = st.sidebar.slider("배합 시간 (분)", 5, 30, 15)

# 3. 가상 데이터 생성 로직 (레오커브 시뮬레이션)
# 온도가 높을수록 반응 속도가 빨라져 그래프가 가파르게 올라간다고 가정
x_time = np.linspace(0, time_mix, 100)
# 가상의 토크 값 계산 (로그 함수 + 노이즈 활용)
y_torque = np.log(x_time + 1) * (temp / 100) + np.random.normal(0, 0.05, 100)

# 4. 품질 예측 모델 (간단한 Rule-based 로직)
# 예: 온도가 140~160도 사이이고, 시간이 10분 이상이어야 '정상'
if 140 <= temp <= 160 and time_mix >= 10:
    prediction = "✅ 적합 (Pass)"
    color = "green"
else:
    prediction = "❌ 부적합 (Fail)"
    color = "red"

# 5. 메인 대시보드 화면 구성
col1, col2 = st.columns(2)

with col1:
    st.subheader("실시간 품질 예측 결과")
    st.markdown(f"## :{color}[{prediction}]")
    st.info(f"현재 설정: 온도 {temp}°C / 시간 {time_mix}분")

with col2:
    st.subheader("모델 적중률 현황")
    # 직무 내용 중 '모델 예측 적중률 비교' 구현
    st.metric(label="최근 24시간 예측 정확도", value="94.5%", delta="1.2%")

# 6. 데이터 시각화 (레오커브 - Matplotlib 활용)
st.subheader("📊 실시간 레오커브(Rheo-curve) 모니터링")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x_time, y_torque, label='Current Batch Torque', color='blue')
ax.axhline(y=1.5, color='r', linestyle='--', label='Target Min Quality') # 품질 기준선
ax.set_title(f"Mixing Process Visualization (Temp: {temp})")
ax.set_xlabel("Time (min)")
ax.set_ylabel("Torque (Nm)")
ax.legend()
st.pyplot(fig)

# 7. 데이터 입력 (작업 후)
st.markdown("---")
st.subheader("2. 작업 후 실측 데이터 입력")
with st.expander("물성 데이터 입력 열기"):
    st.number_input("최종 경도(Hardness) 측정값", min_value=0, max_value=100)
    st.button("데이터 저장")
