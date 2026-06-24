import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import koreanize_matplotlib

st.set_page_config(page_title="동적 GPU 경제성 대시보드", layout="wide")

st.title("동적 GPU 경제성 대시보드")
st.markdown("표를 직접 클릭하여 **값을 수정**하거나, 하단의 표 끝부분을 클릭해 **새로운 지표(행)**를 추가해 보세요. 열(모델) 추가 버튼을 통해서도 확장이 가능합니다.")

# 1. 초기 데이터 세팅 (세션 상태 활용하여 초기화 방지)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        '지표명': ['구매가 (만 달러)', '시장 임대가 ($/hr)', '대표 임대가 ($/hr)'],
        'B200': [3.5, 6.5, 5.0],
        'B300': [4.0, 7.25, 6.0],
        'Rubin': [5.5, 12.0, 11.5]
    })

# 2. 열(모델) 추가 인터페이스
with st.expander("새로운 GPU 모델(열) 추가"):
    col_name = st.text_input("추가할 모델 이름 (예: 차세대 Vera)")
    if st.button("모델 추가") and col_name:
        if col_name not in st.session_state.df.columns:
            st.session_state.df[col_name] = 0.0 # 초기값 0으로 새 열 생성
            st.rerun() # 화면 새로고침

# 3. 동적 데이터 에디터 (행 추가/삭제 및 값 수정)
st.markdown("### 데이터 입력 테이블")
edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic", # 사용자가 자유롭게 행을 추가/삭제할 수 있는 핵심 옵션
    use_container_width=True,
    hide_index=True
)

# 세션 데이터 업데이트
st.session_state.df = edited_df

# 4. 실시간 시각화 렌더링
st.markdown("### 실시간 비교 차트")

# 에디터에서 빈 행이 있을 수 있으므로 결측치 제거
plot_df = edited_df.dropna(subset=['지표명'])
models = [col for col in plot_df.columns if col != '지표명']
metrics = plot_df['지표명'].tolist()

if len(metrics) > 0 and len(models) > 0:
    # 지표 개수에 맞춰 세로로 길게 스크롤하며 볼 수 있도록 1열 다중 행 레이아웃 구성
    fig, axes = plt.subplots(len(metrics), 1, figsize=(10, 4 * len(metrics)))
    
    # 단일 지표일 경우 axes가 리스트가 아니므로 리스트로 변환
    if len(metrics) == 1:
        axes = [axes]
        
    x = np.arange(len(models))
    width = 0.6
    
    # 색상 팔레트 자동 생성 (모델이 추가될 것을 대비)
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % 10) for i in range(len(models))]

    for i, ax in enumerate(axes):
        metric_name = metrics[i]
        values = plot_df.iloc[i][models].astype(float).tolist()
        
        bars = ax.bar(x, values, color=colors, width=width)
        
        ax.set_title(metric_name, fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(models, fontsize=12, fontweight='bold')
        
        # 디자인 정리
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e2e8f0')
        ax.spines['bottom'].set_color('#cbd5e1')
        
        # 라벨 추가
        for j, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height * 1.03, 
                    f"{height:g}", ha='center', va='bottom', 
                    fontsize=12, fontweight='bold', color=colors[j])
            
        ax.set_ylim(0, max(values) * 1.35 if max(values) > 0 else 1)

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("시각화할 데이터가 없습니다. 표에 지표와 모델을 입력해 주세요.")
