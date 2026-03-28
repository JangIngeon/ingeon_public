import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# --- [보안 및 설정] ---
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [UI 설정] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide", initial_sidebar_state="expanded")

# 커스텀 CSS (카드 스타일 및 글꼴 최적화)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- [데이터 수집/분석 함수 - 기존 로직 유지] ---
def get_kamis_data(item_name):
    # (앞선 코드의 get_kamis_data 로직과 동일하게 유지)
    # 보안 어댑터(LegacyPrefixAdapter)를 사용하여 실시간 호출
    pass 

# --- [메인 레이아웃 구성] ---
st.title("🥬 소상공인 식자재 경영 비서")
st.caption("실시간 도매 물가와 기상 데이터를 분석해 사장님의 수익을 지킵니다.")
st.divider()

# 사이드바: 입력 창을 깔끔하게 그룹화
with st.sidebar:
    st.header("⚙️ 설정")
    with st.expander("📌 품목 및 메뉴 정보", expanded=True):
        item_input = st.text_input("분석 품목", value="깻잎")
        usage_input = st.number_input("메뉴 1개당 사용량 (g)", value=50, step=5)
        price_input = st.number_input("현재 메뉴 판매가 (원)", value=12000, step=500)
    
    st.info("💡 실시간 KAMIS API와 연동되어 최신 정보를 가져옵니다.")
    analyze_btn = st.button("🚀 분석 실행", use_container_width=True)

# 메인 화면: 분석 결과 영역
if analyze_btn:
    with st.spinner('🎯 데이터를 정밀 분석 중입니다...'):
        # 1. 데이터 가져오기 & 분석 (예시 데이터 구조 사용)
        # (이 부분에 기존의 raw_price = get_kamis_data(item_input) 및 분석 로직 포함)
        
        # 2. 결과 출력 레이아웃 (3열 지표)
        curr_p, pred_p = 15350, 16400  # 예시 수치
        diff_p = pred_p - curr_p
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
        with m_col2:
            st.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
        with m_col3:
            change_rate = (diff_p / curr_p) * 100
            st.metric("예상 변동률", f"{change_rate:.1f}%")

        st.divider()

        # 3. AI 솔루션 영역 (시각적 강조)
        st.subheader("🤖 사장님을 위한 원가 방어 솔루션")
        
        c_cost = (curr_p / 1000) * usage_input
        f_cost = (pred_p / 1000) * usage_input
        cost_diff = f_cost - c_cost

        # UI 카드 구성
        advice_col1, advice_col2 = st.columns([1.5, 1])
        
        with advice_col1:
            st.markdown(f"""
            ### 📋 요약 리포트
            - **원가 변동**: 한 접시당 원가가 **{c_cost:,.0f}원** → **{f_cost:,.0f}원**으로 변합니다.
            - **상승 원인**: 최근 **일조량 감소 및 기온 급락**이 도매가 상승의 주된 요인입니다.
            - **위험 지수**: <span style='color:red; font-weight:bold;'>주의 (원가율 { (f_cost/price_input)*100:.1f}%)</span>
            """, unsafe_allow_html=True)
            
            st.warning(f"**📢 권장 조치:** 메뉴 가격을 **{round(cost_diff, -1):,.0f}원** 인상하거나, 당분간 {item_input} 대신 저렴한 쌈채소 비중을 높여보세요.")

        with advice_col2:
            # 원가 비중 차트 (간단한 예시)
            chart_data = pd.DataFrame({
                "항목": ["기타 원가", "순이익", item_input],
                "금액": [price_input*0.4, price_input*0.5, f_cost]
            })
            st.write("📊 메뉴 가격 내 원가 비중(예상)")
            st.bar_chart(chart_data.set_index("항목"))

        # 4. 차트 영역
        st.subheader("📈 가격 변동 추이 (최근 1년)")
        # st.line_chart(raw_price.set_index('날짜'))
else:
    st.write("👈 왼쪽 사이드바에서 품목을 입력하고 버튼을 눌러주세요.")
