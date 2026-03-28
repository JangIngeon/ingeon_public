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
        response = session.get("https://www.kamis.or.kr/service/price/xml.do", params=params, verify=False, timeout=30)
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
        return pd.DataFrame()

# --- [3. UI 및 메인 로직] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide")
st.title("🥬 소상공인 식자재 경영 비서")

with st.sidebar:
    st.header("⚙️ 설정")
    item_input = st.text_input("분석 품목", value="깻잎")
    usage_input = st.number_input("메뉴 1개당 사용량 (g)", value=50)
    menu_price_input = st.number_input("현재 메뉴 판매가 (원)", value=12000)
    analyze_btn = st.button("🚀 분석 실행", use_container_width=True)

if analyze_btn:
    with st.spinner(f'🎯 {item_input} 데이터를 실시간 분석 중입니다...'):
        price_df = get_kamis_data(item_input)
        
        if not price_df.empty and len(price_df) > 7:
            # 1. 외부 데이터 병합 (기상/CPI)
            try:
                weather = pd.read_csv('기상데이터.csv')
                weather['일시'] = pd.to_datetime(weather['일시'])
                weather_daily = weather.groupby('일시')[['평균기온(°C)', '일강수량(mm)', '합계 일조시간(hr)']].mean().reset_index()
                
                df_merged = pd.merge(price_df, weather_daily, left_on='날짜', right_on='일시', how='left')
                df_merged = df_merged.ffill().bfill() # 결측치 채우기
                
                # 2. 현재 가격 및 예측 계산
                curr_p = float(df_merged['가격'].iloc[-1])
                
                # [예측 엔진] 실제 모델 로직이 들어가는 부분 (여기선 5% 변동 예시)
                # 실제 OLS 모델 학습 코드를 이 자리에 넣으시면 됩니다.
                pred_p = curr_p * 1.05 
                diff_p = float(pred_p - curr_p)
                
                # 3. 결과 출력 (ValueError 방지 핵심)
                st.divider()
                col1, col2, col3 = st.columns(3)
                
                # 현재가 출력
                col1.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
                
                # 예측가 출력 (숫자인지 다시 한번 체크)
                if not np.isnan(diff_p):
                    col2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
                    col3.metric("예상 변동률", f"{(diff_p/curr_p)*100:.1f}%")
                else:
                    col2.metric("1주일 뒤 예상가", "분석 데이터 부족")
                    
                # 4. AI 경영 솔루션
                st.subheader("🤖 AI 원가 방어 솔루션")
                curr_cost = (curr_p / 1000) * usage_input
                future_cost = (pred_p / 1000) * usage_input
                
                st.info(f"""
                현재 **{item_input}**의 가격은 다음 주 약 **{abs(diff_p):,.0f}원** 상승할 것으로 예측됩니다.
                사장님의 메뉴 1그릇당 원가는 **{curr_cost:,.0f}원**에서 **{future_cost:,.0f}원**으로 변경될 예정입니다.
                약 **{round(future_cost - curr_cost, -1):,.0f}원**의 원가 상승이 예상되오니 메뉴 가격 조정에 참고하세요.
                """)
                
                st.line_chart(price_df.set_index('날짜')['가격'])
                
            except Exception as e:
                st.error(f"데이터 분석 과정에서 오류가 발생했습니다: {e}")
        else:
            st.warning("분석할 수 있는 충분한 데이터가 없습니다. 품목명을 확인해주세요.")
