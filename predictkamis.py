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

# --- [1. 보안 및 SSL 설정] ---
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [2. 데이터 수집 함수] ---
def get_kamis_data(item_name):
    try:
        df_map = pd.read_csv('농축수산물 품목 및 등급 코드표.csv')
        target = df_map[df_map['품목명'] == item_name].iloc[0]
        
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

        session = requests.Session()
        session.mount("https://", LegacyPrefixAdapter())
        response = session.get("https://www.kamis.or.kr/service/price/xml.do", params=params, verify=False, timeout=30)
        root = ET.fromstring(response.content)
        
        data_list = []
        for item in root.findall(".//data/item"):
            if item.findtext('countyname') == '평균':
                p_text = item.findtext('price').replace(',', '')
                if p_text == '-': continue
                data_list.append({"날짜": f"{item.findtext('yyyy')}-{item.findtext('regday').replace('/', '-')}", "가격": int(p_text)})
        
        res_df = pd.DataFrame(data_list)
        if not res_df.empty:
            res_df['날짜'] = pd.to_datetime(res_df['날짜'])
            return res_df.sort_values('날짜')
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# --- [3. UI 및 메인 로직] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide")
st.title("🥬 소상공인 식자재 경영 비서")

with st.sidebar:
    st.header("⚙️ 설정")
    item_input = st.text_input("분석 품목", value="깻잎")
    usage_input = st.sidebar.number_input("메뉴 1개당 사용량 (g)", value=50)
    menu_p_input = st.sidebar.number_input("현재 메뉴 판매가 (원)", value=12000)
    analyze_btn = st.sidebar.button("🚀 분석 실행")

if analyze_btn:
    with st.spinner(f'🎯 {item_input} 데이터를 실시간 분석 중입니다...'):
        price_df = get_kamis_data(item_input)
        
        if not price_df.empty and len(price_df) > 10:
            # 현재 가격 설정
            curr_p = float(price_df['가격'].iloc[-1])
            
            # --- [예측 엔진: 이 부분에 모델 로직 결합] ---
            # 실제 모델 학습 코드가 들어가는 곳입니다. 
            # 에러 방지를 위해 변수를 미리 0으로 초기화하고 계산합니다.
            pred_p = 0.0
            diff_p = 0.0
            
            try:
                # 여기에 기존에 작성했던 OLS 모델 학습 및 pred_p 계산 코드를 넣으세요.
                # 예시로 5% 상승 로직을 넣었습니다.
                pred_p = curr_p * 1.05 
                diff_p = pred_p - curr_p
            except:
                pred_p = curr_p
                diff_p = 0.0

            # --- [UI 출력부: 에러 발생 지점] ---
            st.divider()
            c1, c2, c3 = st.columns(3)
            
            # 수치 데이터가 확실히 Float인지 확인하며 출력
            c1.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
            
            # diff_p가 정상적인 숫자인 경우에만 출력
            if not np.isnan(diff_p):
                c2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
                c3.metric("예상 변동률", f"{(diff_p/curr_p)*100:.1f}%")
            else:
                c2.metric("1주일 뒤 예상가", "분석 불가")

            # --- [AI 경영 솔루션] ---
            st.subheader("🤖 AI 원가 방어 솔루션")
            curr_cost = (curr_p / 1000) * usage_input
            future_cost = (pred_p / 1000) * usage_input
            
            st.info(f"""
            현재 **{item_input}**의 가격은 다음 주 약 **{abs(diff_p):,.0f}원** 변동할 것으로 예측됩니다.
            사장님의 메뉴 1그릇당 원가는 **{curr_cost:,.0f}원**에서 **{future_cost:,.0f}원**으로 변경될 예정입니다.
            """)
            
            st.line_chart(price_df.set_index('날짜')['가격'])
        else:
            st.error("데이터가 부족하거나 불러오지 못했습니다. 품목명을 확인해주세요.")
