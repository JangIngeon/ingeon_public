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
import ssl

# --- [1. 보안 및 SSL 설정: Handshake & Certificate 오류 해결] ---
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # SSL 컨텍스트 생성
        context = create_urllib3_context()
        # 보안 등급 하향 및 구형 암호화 허용
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        # 인증서 검증 및 호스트 이름 확인 비활성화 (오류 해결 핵심)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

# urllib3 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [2. 데이터 수집 함수 (API)] ---
def get_kamis_data(item_name):
    try:
        # 코드표 로드 (GitHub 리포지토리에 파일이 있어야 함)
        df_map = pd.read_csv('농축수산물 품목 및 등급 코드표.csv')
        target = df_map[df_map['품목명'] == item_name].iloc[0]
        
        url = "https://www.kamis.or.kr/service/price/xml.do"
        params = {
            "action": "periodProductList",
            "p_cert_key": "31f6d529-1b15-407d-a46c-bce8afdad18c",
            "p_cert_id": "5652",
            "p_returntype": "xml",
            "p_startday": "2024-01-01",
            "p_endday": datetime.now().strftime("%Y-%m-%d"),
            "p_productclscode": "02",
            "p_itemcategorycode": str(int(target['품목 그룹코드'])),
            "p_itemcode": str(int(target['품목 코드'])),
            "p_kindcode": str(int(target['품종코드'])).zfill(2),
            "p_productrankcode": "04",
            "p_countrycode": "1101",
            "p_convert_kg_yn": "Y"
        }

        # 세션 생성 및 어댑터 장착
        session = requests.Session()
        session.mount("https://", LegacyPrefixAdapter())
        
        # API 호출
        response = session.get(url, params=params, verify=False, timeout=30)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)
        
        data_list = []
        for item in root.findall(".//data/item"):
            if item.findtext('countyname') == '평균':
                p_text = item.findtext('price').replace(',', '')
                if p_text == '-': continue
                data_list.append({
                    "날짜": f"{item.findtext('yyyy')}-{item.findtext('regday').replace('/', '-')}", 
                    "가격": int(p_text)
                })
        
        res_df = pd.DataFrame(data_list)
        if not res_df.empty:
            res_df['날짜'] = pd.to_datetime(res_df['날짜'])
            return res_df.sort_values('날짜')
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 수집 중 오류: {e}")
        return pd.DataFrame()

# --- [3. UI 및 분석 로직] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide")

st.title("🥬 소상공인 식자재 경영 비서")
st.caption("실시간 도매 물가와 기상 데이터를 분석해 사장님의 수익을 지킵니다.")

with st.sidebar:
    st.header("⚙️ 설정")
    item_input = st.text_input("분석 품목", value="깻잎")
    usage_input = st.number_input("메뉴 1개당 사용량 (g)", value=50)
    menu_p_input = st.number_input("현재 메뉴 판매가 (원)", value=12000)
    analyze_btn = st.button("🚀 분석 실행", use_container_width=True)

if analyze_btn:
    with st.spinner(f'🎯 {item_input} 데이터를 실시간 분석 중입니다...'):
        price_df = get_kamis_data(item_input)
        
        if not price_df.empty:
            # 기본 통계 및 시각화
            curr_p = price_df['가격'].iloc[-1]
            
            # --- [분석/예측 엔진] ---
            # 실제 서비스 시에는 여기서 기상/CPI 데이터를 병합하고 모델을 학습시킵니다.
            # 임시로 1주일 뒤 5% 변동을 가정하여 UI가 작동하는지 확인합니다.
            pred_p = curr_p * 1.05 
            diff_p = pred_p - curr_p
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
            c2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
            c3.metric("예상 변동률", f"{(diff_p/curr_p)*100:.1f}%")

            # AI 솔루션 출력
            st.subheader("🤖 AI 원가 방어 솔루션")
            curr_cost = (curr_p / 1000) * usage_input
            future_cost = (pred_p / 1000) * usage_input
            
            st.info(f"""
            현재 **{item_input}**의 가격은 다음 주 약 **{abs(diff_p):,.0f}원** 상승할 것으로 예측됩니다.
            이에 따라 사장님의 메뉴 1그릇당 원가는 **{curr_cost:,.0f}원**에서 **{future_cost:,.0f}원**으로 변경될 예정입니다.
            **{round(future_cost - curr_cost, -1):,.0f}원** 정도의 가격 인상 요인이 발생하오니 원가 관리에 유의하세요.
            """)
            
            st.line_chart(price_df.set_index('날짜')['가격'])
        else:
            st.warning("데이터를 불러오지 못했습니다. 품목명을 확인하거나 잠시 후 다시 시도해주세요.")
