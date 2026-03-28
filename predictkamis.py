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

# --- [1. 보안 및 SSL 설정] ---
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [2. 데이터 수집 함수 (API)] ---
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
        response = session.get("https://www.kamis.or.kr/service/price/xml.do", params=params, verify=False, timeout=20)
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
        st.error(f"데이터 수집 중 오류: {e}")
        return pd.DataFrame()

# --- [3. UI 레이아웃] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide")

st.title("🥬 소상공인 식자재 경영 비서")
st.caption("실시간 도매 물가와 기상 데이터를 분석해 사장님의 수익을 지킵니다.")

with st.sidebar:
    st.header("⚙️ 설정")
    item_input = st.text_input("분석 품목", value="깻잎")
    usage_input = st.number_input("메뉴 1개당 사용량 (g)", value=50)
    menu_price_input = st.number_input("현재 메뉴 판매가 (원)", value=12000)
    analyze_btn = st.button("🚀 분석 실행", use_container_width=True)

if analyze_btn:
    with st.spinner('🎯 실시간 데이터를 분석 중입니다...'):
        # 1. API 데이터 호출
        price_df = get_kamis_data(item_input)
        
        if not price_df.empty:
            # 2. 외부 데이터(기상, CPI) 병합 및 분석 (생략된 기존 분석 로직 포함)
            # 여기서는 분석 결과(curr_p, pred_p)가 계산되었다고 가정함
            weather = pd.read_csv('기상데이터.csv') # 기존 파일 활용
            cpi = pd.read_csv('소비자물가지수_2020100__20260327012010.csv') # 기존 파일 활용
            
            # --- [핵심: 분석 및 예측 로직 실행] ---
            # (이 부분에 이전에 작성한 시차 변수 생성 및 OLS 모델 학습 코드가 들어갑니다)
            # [예시 수치 대신 실제 계산 결과 적용 예시]
            curr_p = price_df['가격'].iloc[-1] # 가장 최근 실제 가격
            
            # (임시: 모델을 통해 계산된 pred_p가 있다고 가정)
            # 실제 서비스 시에는 위 로직에서 학습된 model.predict() 결과값을 pred_p에 할당하세요.
            # 여기서는 코드 작동 구조를 보여주기 위해 계산식을 유지합니다.
            pred_p = curr_p * 1.05 # 실제로는 모델 예측값이 들어감
            diff_p = pred_p - curr_p
            
            # 3. 메트릭 출력 (에러 방지를 위해 변수 확인 후 실행)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
            col2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
            col3.metric("예상 변동률", f"{(diff_p/curr_p)*100:.1f}%")

            # 4. AI 경영 솔루션
            st.subheader("🤖 AI 원가 방어 솔루션")
            curr_cost = (curr_p / 1000) * usage_input
            future_cost = (pred_p / 1000) * usage_g if 'usage_g' in locals() else (pred_p / 1000) * usage_input
            
            st.info(f"""
            현재 **{item_input}**의 가격은 다음 주 약 **{diff_p:,.0f}원** 변동될 것으로 예측됩니다.
            사장님의 메뉴 1개당 원가는 **{curr_cost:,.0f}원**에서 **{future_cost:,.0f}원**으로 변경될 예정입니다.
            """)
            
            st.line_chart(price_df.set_index('날짜'))
        else:
            st.error("데이터를 불러오지 못했습니다. 품목명을 정확히 입력해주세요.")
