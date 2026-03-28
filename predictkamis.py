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

# --- [1. 보안 및 SSL 설정: 공공데이터 API 연결용] ---
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [2. 인코딩 자동 해결 파일 로드 함수] ---
def safe_read_csv(file_name):
    for enc in ['utf-8', 'cp949', 'euc-kr']:
        try:
            return pd.read_csv(file_name, encoding=enc)
        except:
            continue
    st.error(f"❌ {file_name} 파일을 읽을 수 없습니다. 인코딩을 확인하세요.")
    return None

# --- [3. KAMIS API 데이터 수집 함수] ---
def get_kamis_data(item_name):
    try:
        df_map = safe_read_csv('농축수산물 품목 및 등급 코드표.csv')
        if df_map is None: return pd.DataFrame()
        
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

# --- [4. UI 및 메인 로직] ---
st.set_page_config(page_title="식자재 원가 비서", layout="wide")
st.title("🥬 소상공인 식자재 경영 비서")
st.caption("실시간 물가와 기상 데이터를 분석해 최적의 가격 전략을 제안합니다.")

with st.sidebar:
    st.header("⚙️ 설정")
    item_input = st.text_input("분석 품목", value="깻잎")
    usage_input = st.number_input("메뉴 1개당 사용량 (g)", value=50)
    menu_p_input = st.number_input("현재 메뉴 판매가 (원)", value=12000)
    analyze_btn = st.button("🚀 분석 실행", use_container_width=True)

if analyze_btn:
    with st.spinner(f'🎯 {item_input} 데이터를 실시간 분석 중입니다...'):
        price_df = get_kamis_data(item_input)
        
        if not price_df.empty and len(price_df) > 10:
            try:
                # 데이터 로드
                weather = safe_read_csv('기상데이터.csv')
                cpi = safe_read_csv('소비자물가지수_2020100__20260327012010.csv')
                
                # 기상 데이터 전처리
                weather['일시'] = pd.to_datetime(weather['일시'])
                w_daily = weather.groupby('일시')[['평균기온(°C)', '일강수량(mm)', '합계 일조시간(hr)']].mean().reset_index()
                
                # CPI 전처리
                cpi_long = cpi.melt(id_vars=['시도별'], var_name='Month', value_name='CPI_지수')
                cpi_long['Month'] = pd.to_datetime(cpi_long['Month'], format='%Y.%m')
                cpi_nat = cpi_long[cpi_long['시도별'] == '전국'].copy()

                # 데이터 병합
                df = pd.merge(price_df, w_daily, left_on='날짜', right_on='일시', how='left')
                df['YearMonth'] = df['날짜'].dt.to_period('M').dt.to_timestamp()
                df = pd.merge(df, cpi_nat[['Month', 'CPI_지수']], left_on='YearMonth', right_on='Month', how='left')
                df = df.ffill().bfill() # 결측치 보정

                # 파생 변수 생성
                base_p = df['가격'].iloc[0]
                df['품목_지수'] = (df['가격'] / base_p) * 100
                df['기온_7일_평균'] = df['평균기온(°C)'].rolling(window=7).mean()
                df['강수량_30일_누적'] = df['일강수량(mm)'].rolling(window=30).sum()
                df['일조_14일_평균'] = df['합계 일조시간(hr)'].rolling(window=14).mean()
                df['지수_7일후'] = df['품목_지수'].shift(-7)

                # 회귀 모델 학습 (OLS)
                features = ['평균기온(°C)', '강수량_30일_누적', '일조_14일_평균', 'CPI_지수', '품목_지수']
                df_train = df.dropna(subset=features + ['지수_7일후'])
                
                if not df_train.empty:
                    X = sm.add_constant(df_train[features])
                    y = df_train['지수_7일후']
                    model = sm.OLS(y, X).fit()

                    # 예측 수행
                    latest_row = df.dropna(subset=features).tail(1)
                    X_now = sm.add_constant(latest_row[features], has_constant='add')
                    pred_idx = model.predict(X_now)[0]
                    
                    curr_p = float(latest_row['가격'].iloc[0])
                    pred_p = (pred_idx * base_p) / 100
                    diff_p = float(pred_p - curr_p)
                    top_factor = model.pvalues.idxmin() # 가장 영향력 큰 변수

                    # --- [결과 출력] ---
                    st.divider()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("현재 도매가 (1kg)", f"{curr_p:,.0f}원")
                    if not np.isnan(diff_p):
                        c2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{diff_p:+,0f}원", delta_color="inverse")
                        c3.metric("예상 변동률", f"{(diff_p/curr_p)*100:.1f}%")

                    # AI 솔루션
                    st.subheader("🤖 AI 원가 방어 솔루션")
                    curr_cost = (curr_p / 1000) * usage_input
                    future_cost = (pred_p / 1000) * usage_input
                    
                    st.info(f"""
                    분석 결과, 최근 **{top_factor}**의 영향으로 {item_input} 가격이 다음 주 약 **{abs(diff_p):,.0f}원** 변동할 것으로 예측됩니다.
                    사장님의 메뉴 1그릇당 원가는 **{curr_cost:,.0f}원**에서 **{future_cost:,.0f}원**으로 변경될 예정입니다.
                    **{round(future_cost - curr_cost, -1):,.0f}원** 정도의 가격 인상 요인이 발생하오니 참고하세요.
                    """)
                    
                    st.line_chart(price_df.set_index('날짜')['가격'])
                else:
                    st.warning("분석을 위한 학습 데이터가 부족합니다.")

            except Exception as e:
                st.error(f"분석 엔진 실행 중 오류 발생: {e}")
        else:
            st.error("데이터가 부족하거나 불러오지 못했습니다. 품목명을 확인해주세요.")
