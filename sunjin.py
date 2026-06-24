import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import koreanize_matplotlib
import requests

# 웹 페이지 기본 설정
st.set_page_config(page_title="NVIDIA GPU 경제성 지표 대시보드", layout="wide")

st.title("📊 NVIDIA 차세대 AI 인프라 경제성 대시보드")
st.markdown("노션(Notion) 데이터베이스의 수치를 실시간으로 반영하여 비교하는 대시보드이다.")

# --------------------------------------------------------
# [API 설정] 본인이 발급받은 노션 API 정보로 교체해야 한다.
# --------------------------------------------------------
NOTION_TOKEN = "secret_본인의_노션_토큰을_여기에_입력"
DATABASE_ID = "본인의_노션_데이터베이스_ID를_여기에_입력"

# 데이터 캐싱 (버튼 누를 때만 새로고침 되도록 설정)
@st.cache_data
def fetch_notion_data():
    """
    노션 API를 호출하여 데이터를 가져오는 함수이다.
    초기 테스트를 위해 API 토큰이 없으면 임시 기본 데이터를 반환하도록 방어 코드를 작성했다.
    """
    if NOTION_TOKEN.startswith("secret_본인"):
        # API 설정이 안 되어 있을 경우 띄워줄 기본(Mock) 데이터
        return {
            "models": ['B200', 'B300', 'Rubin'],
            "data": [
                [(3.5, 3.5), (4.0, 4.0), (5.5, 5.5)],    # 구매가
                [(2.1, 11.0), (2.5, 12.0), (6.0, 16.0)], # 시장 임대가
                [(5.0, 5.0), (6.0, 6.0), (8.0, 15.0)]    # 대표 임대가
            ],
            "labels": [
                ['약 $3.5만', '약 $4만', '약 $5.5만'],
                ['$2.1~11', '$2.5~12', '$6~10+(업계)\n$8~16(AI계산)'],
                ['$5', '$6', '$8~15']
            ]
        }
    
    # --------------------------------------------------------
    # [실제 노션 API 호출 로직]
    # 노션 표의 구조(속성 이름 등)에 맞게 파싱 로직을 수정하여 사용한다.
    # --------------------------------------------------------
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    response = requests.post(url, headers=headers)
    results = response.json().get("results", [])
    
    # (주의) 여기에 노션 JSON 응답을 파싱하여 위의 기본 데이터 형태로 
    # 가공하는 파이썬 로직을 추가해야 완벽히 연동된다.
    pass

# 상단 새로고침 버튼 배치
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("🔄 데이터 최신화"):
        st.cache_data.clear() # 캐시를 비워 다음 호출 시 노션 데이터를 다시 읽어옴

# 데이터 로딩
notion_data = fetch_notion_data()
models = notion_data["models"]
data = notion_data["data"]
labels = notion_data["labels"]

colors = ['#2563eb', '#f59e0b', '#10b981']
light_colors = ['#bfdbfe', '#fde68a', '#a7f3d0']
metrics = ['구매가\n(단일 GPU 1개 기준, 만 달러)', '시장 임대가\n($/GPU-hr)', '대표 임대가\n($/GPU-hr)']

# --------------------------------------------------------
# 시각화 렌더링 영역 (Matplotlib)
# --------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 7))

x = np.arange(len(models))
width = 0.6

for i, ax in enumerate(axes):
    ax.set_title(metrics[i], fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=13, fontweight='bold')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e2e8f0')
    ax.spines['bottom'].set_color('#cbd5e1')
    ax.tick_params(axis='y', colors='#64748b')

    max_height_for_ylim = 0

    for j in range(len(models)):
        min_v, max_v = data[i][j]
        color = colors[j]
        light_color = light_colors[j]
        
        # 1) 기본 진한 막대
        ax.bar(x[j], min_v, width=width, color=color)
        
        # 2) 범위 연한 막대 누적
        if max_v > min_v:
            ax.bar(x[j], max_v - min_v, bottom=min_v, width=width, 
                   color=light_color, edgecolor=color, linewidth=1.5) 
            
        if max_v > max_height_for_ylim:
            max_height_for_ylim = max_v
            
        # 텍스트 라벨 추가
        ax.text(x[j], max_v * 1.03, labels[i][j], ha='center', va='bottom', 
                fontsize=12, fontweight='bold', color=color, linespacing=1.3)
    
    ax.set_ylim(0, max_height_for_ylim * 1.35)

plt.tight_layout(rect=[0, 0, 1, 0.95])

# Streamlit 화면에 그래프 출력
st.pyplot(fig)
