import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib3

# SSL 인증서 경고 무시 설정 (KAMIS API 연결용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="소상공인 식자재 원가 비서", layout="wide")

st.title("🥬 실시간 식자재 가격 예측 & 경영 솔루션")
st.markdown("전국 도매가격 실시간 데이터를 기반으로 사장님의 메뉴 원가와 미래 가격을 분석합니다.")

# --- 2. KAMIS API 데이터 수집 함수 (SSL 오류 수정 버전) ---
def get_kamis_perfect_data(item_name, start_date="2024-01-01", end_date=None):
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # 코드표 로드 (CSV 파일이 GitHub 리포지토리에 함께 있어야 함)
        df_map = pd.read_csv('농축수산물 품목 및 등급 코드표.csv')
        target = df_map[df_map['품목명'] == item_name].iloc[0]
        
        c_code = str(int(target['품목 그룹코드']))
        i_code = str(int(target['품목 코드']))
        k_code = str(int(target['품종코드'])).zfill(2)

        url = "https://www.kamis.or.kr/service/price/xml.do"
        params = {
            "action": "periodProductList",
            "p_cert_key": "31f6d529-1b15-407d-a46c-bce8afdad18c",
            "p_cert_id": "5652",
            "p_returntype": "xml",
            "p_startday": start_date,
            "p_endday": end_date,
            "p_productclscode": "02",      # 도매 기준
            "p_itemcategorycode": c_code,
            "p_itemcode": i_code,
            "p_kindcode": k_code,
            "p_productrankcode": "04",     # 상품(上) 등급
            "p_countrycode": "1101",       # 서울 지역
            "p_convert_kg_yn": "Y"
        }

        # verify=False 를 추가하여 SSL 핸드셰이크 오류 방지
        response = requests.get(url, params=params, verify=False, timeout=20)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)
        
        data_list = []
        for item in root.findall(".//data/item"):
            if item.findtext('countyname') == '평균':
                price_text = item.findtext('price').replace(',', '')
                if price_text == '-': continue
                data_list.append({
                    "날짜": f"{item.findtext('yyyy')}-{item.findtext('regday').replace('/', '-')}",
                    "가격(1kg)": int(price_text)
                })
        
        result_df = pd.DataFrame(data_list)
        if not result_df.empty:
            result_df['날짜'] = pd.to_datetime(result_df['날짜'])
            return result_df.sort_values('날짜')
        return pd.DataFrame()
    except Exception as e:
        st.error(f"API 호출 중 오류 발생: {e}")
        return pd.DataFrame()

# --- 3. 데이터 분석 및 변수 생성 함수 ---
def analyze_data(price_df):
    # 외부 데이터 로드 (기상, CPI) - 파일이 리포지토리에 있어야 함
    weather = pd.read_csv('기상데이터.csv')
    cpi = pd.read_csv('소비자물가지수_2020100__20260327012010.csv')
    
    weather['일시'] = pd.to_datetime(weather['일시'])
    weather_daily = weather.groupby('일시')[['평균기온(°C)', '일강수량(mm)', '합계 일조시간(hr)']].mean().reset_index()
    
    cpi_long = cpi.melt(id_vars=['시도별'], var_name='Month', value_name='CPI_지수')
    cpi_long['Month'] = pd.to_datetime(cpi_long['Month'], format='%Y.%m')
    cpi_nat = cpi_long[cpi_long['시도별'] == '전국'].copy()

    df = pd.merge(price_df, weather_daily, left_on='날짜', right_on='일시', how='left')
    df['YearMonth'] = df['날짜'].dt.to_period('M').dt.to_timestamp()
    df = pd.merge(df, cpi_nat[['Month', 'CPI_지수']], left_on='YearMonth', right_on='Month', how='left')

    # 파생 변수 생성
    base_p = df['가격(1kg)'].iloc[0]
    df['품목_지수'] = (df['가격(1kg)'] / base_p) * 100
    df['기온_7일_평균'] = df['평균기온(°C)'].rolling(window=7).mean()
    df['강수량_30일_누적'] = df['일강수량(mm)'].rolling(window=30).sum()
    df['일조_14일_평균'] = df['합계 일조시간(hr)'].rolling(window=14).mean()
    df['지수_7일후'] = df['품목_지수'].shift(-7)
    
    return df.dropna(subset=['강수량_30일_누적']), base_p

# --- 4. 메인 화면 ---
st.sidebar.header("🔍 분석 설정")
item_name = st.sidebar.text_input("조회할 품목명", value="깻잎")
usage_g = st.sidebar.number_input("음식 1개당 사용량 (g)", value=50)
current_menu_price = st.sidebar.number_input("현재 메뉴 판매가 (원)", value=12000)

if st.sidebar.button("실시간 예측 실행"):
    with st.spinner(f'{item_name} 데이터를 분석 중입니다...'):
        price_raw = get_kamis_perfect_data(item_name)
        
        if not price_raw.empty:
            df_final, base_val = analyze_data(price_raw)
            
            # 회귀 모델 학습
            features = ['평균기온(°C)', '강수량_30일_누적', '일조_14일_평균', 'CPI_지수', '품목_지수']
            df_train = df_final.dropna(subset=['지수_7일후'])
            
            if len(df_train) > 10: # 최소 데이터 확인
                X = sm.add_constant(df_train[features])
                y = df_train['지수_7일후']
                model = sm.OLS(y, X).fit()
                
                latest = df_final.tail(1)
                X_now = sm.add_constant(latest[features], has_constant='add')
                pred_idx = model.predict(X_now)[0]
                
                curr_p = latest['가격(1kg)'].values[0]
                pred_p = (pred_idx * base_val) / 100
                
                col1, col2 = st.columns(2)
                col1.metric(f"현재 {item_name} 도매가 (1kg)", f"{curr_p:,.0f}원")
                col2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{pred_p - curr_p:,.0f}원")

                # AI 컨설팅 솔루션
                st.subheader("🤖 사장님을 위한 AI 경영 솔루션")
                curr_cost = (curr_p / 1000) * usage_g
                pred_cost = (pred_p / 1000) * usage_g
                increase = pred_cost - curr_cost
                
                top_var = model.pvalues.idxmin() # 가장 영향력 큰 변수

                st.info(f"""
                최근 **{top_var}**의 변화 영향으로 인해 **{item_name}**의 도매가가 일주일 뒤 약 **{abs(pred_p - curr_p):,.0f}원** 변동할 것으로 예측됩니다.
                
                이에 따라 사장님이 만드시는 메뉴 한 그릇당 원가는 현재 **{curr_cost:,.0f}원**에서 일주일 뒤 **{pred_cost:,.0f}원**으로 변경될 예정입니다.
                
                **[가격 전략 제안]**
                - 원가 보전을 위해 메뉴 가격을 약 **{round(increase, -1):,.0f}원** 정도 인상하는 것을 고려해 보세요.
                - 단, 고객 이탈을 막기 위해 500원 이상의 급격한 가격 인상보다는 사이드 메뉴 구성을 조정하는 것을 추천합니다.
                """)
                
                st.line_chart(price_raw.set_index('날짜')['가격(1kg)'])
            else:
                st.warning("분석을 위한 데이터량이 충분하지 않습니다.")
        else:
            st.error("데이터를 불러오지 못했습니다. 품목명이나 API 설정을 확인해주세요.")
