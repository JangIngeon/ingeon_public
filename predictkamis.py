import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib3

# [보안 설정] SSL 인증서 검증 오류 방지 (KAMIS API 연결용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="소상공인 식자재 원가 비서", layout="wide", page_icon="🥬")

st.title("🥬 실시간 식자재 가격 예측 & 경영 솔루션")
st.markdown("""
이 서비스는 **KAMIS 실시간 도매가**와 **기상 정보**를 분석하여 미래 가격을 예측합니다.  
사장님의 메뉴 사용량을 입력하시면 **맞춤형 원가 방어 전략**을 제안해 드립니다.
""")

# --- 2. KAMIS API 실시간 데이터 수집 함수 ---
def get_kamis_data(item_name, start_date="2024-01-01"):
    end_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # 품목 코드표 로드 (CSV 파일이 리포지토리에 함께 있어야 함)
        df_map = pd.read_csv('농축수산물 품목 및 등급 코드표.csv')
        target = df_map[df_map['품목명'] == item_name].iloc[0]
        
        c_code = str(int(target['품목 그룹코드']))
        i_code = str(int(target['품목 코드']))
        k_code = str(int(target['품종코드'])).zfill(2)

        url = "https://www.kamis.or.kr/service/price/xml.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
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

        # SSL 검증 무시(verify=False) 및 타임아웃 설정으로 Handshake 오류 방지
        response = requests.get(url, params=params, headers=headers, verify=False, timeout=20)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        root = ET.fromstring(response.content)
        
        data_list = []
        for item in root.findall(".//data/item"):
            if item.findtext('countyname') == '평균':
                p_text = item.findtext('price').replace(',', '')
                if p_text == '-': continue
                data_list.append({
                    "날짜": f"{item.findtext('yyyy')}-{item.findtext('regday').replace('/', '-')}",
                    "가격(1kg)": int(p_text)
                })
        
        res_df = pd.DataFrame(data_list)
        if not res_df.empty:
            res_df['날짜'] = pd.to_datetime(res_df['날짜'])
            return res_df.sort_values('날짜')
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# --- 3. 데이터 분석 및 모델링 함수 ---
def run_analysis(price_df):
    # 기존 업로드한 기상 및 CPI 파일 활용
    weather = pd.read_csv('기상데이터.csv')
    cpi = pd.read_csv('소비자물가지수_2020100__20260327012010.csv')
    
    # 기상/CPI 전처리
    weather['일시'] = pd.to_datetime(weather['일시'])
    weather_daily = weather.groupby('일시')[['평균기온(°C)', '일강수량(mm)', '합계 일조시간(hr)']].mean().reset_index()
    cpi_long = cpi.melt(id_vars=['시도별'], var_name='Month', value_name='CPI_지수')
    cpi_long['Month'] = pd.to_datetime(cpi_long['Month'], format='%Y.%m')
    cpi_nat = cpi_long[cpi_long['시도별'] == '전국'].copy()

    # 데이터 병합
    df = pd.merge(price_df, weather_daily, left_on='날짜', right_on='일시', how='left')
    df['YearMonth'] = df['날짜'].dt.to_period('M').dt.to_timestamp()
    df = pd.merge(df, cpi_nat[['Month', 'CPI_지수']], left_on='YearMonth', right_on='Month', how='left')

    # 파생 변수 생성 (기존 로직)
    base_p = df['가격(1kg)'].iloc[0]
    df['품목_지수'] = (df['가격(1kg)'] / base_p) * 100
    df['기온_7일_평균'] = df['평균기온(°C)'].rolling(window=7).mean()
    df['강수량_30일_누적'] = df['일강수량(mm)'].rolling(window=30).sum()
    df['일조_14일_평균'] = df['합계 일조시간(hr)'].rolling(window=14).mean()
    df['지수_7일후'] = df['품목_지수'].shift(-7)
    
    return df.dropna(subset=['강수량_30일_누적']), base_p

# --- 4. 사용자 인터페이스 (Streamlit UI) ---
st.sidebar.header("📍 사장님 정보 입력")
item_to_find = st.sidebar.text_input("분석 품목 (예: 깻잎, 상추, 배추)", value="깻잎")
user_usage = st.sidebar.number_input("메뉴 1개당 사용량 (g)", min_value=1, value=50)
user_menu_p = st.sidebar.number_input("현재 판매가 (원)", min_value=0, value=12000)

if st.sidebar.button("📊 실시간 분석 및 결과 보기"):
    with st.spinner(f'{item_to_find}의 최신 데이터를 수집하고 분석 중입니다...'):
        raw_price = get_kamis_data(item_to_find)
        
        if not raw_price.empty:
            df_ml, base_val = run_analysis(raw_price)
            
            # 회귀 모델 학습 (7일 뒤 예측)
            feats = ['평균기온(°C)', '강수량_30일_누적', '일조_14일_평균', 'CPI_지수', '품목_지수']
            df_train = df_ml.dropna(subset=['지수_7일후'])
            
            if len(df_train) > 5:
                X = sm.add_constant(df_train[feats])
                y = df_train['지수_7일후']
                model = sm.OLS(y, X).fit()
                
                # 오늘 데이터를 바탕으로 1주일 뒤 예측
                latest = df_ml.tail(1)
                X_now = sm.add_constant(latest[feats], has_constant='add')
                pred_idx = model.predict(X_now)[0]
                
                curr_p = latest['가격(1kg)'].values[0]
                pred_p = (pred_idx * base_val) / 100
                
                # 주요 지표 대시보드
                c1, c2 = st.columns(2)
                c1.metric(f"현재 {item_to_find} 도매가 (1kg)", f"{curr_p:,.0f}원")
                c2.metric("1주일 뒤 예상가", f"{pred_p:,.0f}원", f"{pred_p - curr_p:,.0f}원")

                # --- AI 경영 솔루션 리포트 ---
                st.subheader("🤖 사장님을 위한 AI 경영 솔루션")
                
                c_cost = (curr_p / 1000) * user_usage
                f_cost = (pred_p / 1000) * user_usage
                diff = f_cost - c_cost
                
                # 통계적 유의미한 변수 추출
                top_v = model.pvalues.idxmin()

                st.info(f"""
                분석 결과, 최근 **{top_v}**의 변화가 **{item_to_find}** 가격 변동의 주요 원인으로 파악됩니다. 
                이로 인해 다음 주 도매가는 현재보다 약 **{abs(pred_p - curr_p):,.0f}원** 상승할 것으로 보입니다.

                **[원가 분석 결과]**
                사장님의 메뉴 1그릇당 {item_to_find} 원가는 현재 **{c_cost:,.0f}원**에서 일주일 뒤 **{f_cost:,.0f}원**으로 변경될 예정입니다.

                **[AI 가격 전략 가이드]**
                - 원가 보전을 위해 메뉴 가격을 약 **{round(diff, -1):,.0f}원** 인상하는 것을 고려해 보세요.
                - 단, 고객 이탈 위험을 최소화하기 위해 **500원 이상의 급격한 인상**보다는 세트 메뉴 구성 변경이나 양 조절을 통한 '스텔스 원가 절감' 전략을 추천드립니다.
                """)
                
                st.subheader("📈 최근 가격 변동 추이")
                st.line_chart(raw_price.set_index('날짜')['가격(1kg)'])
            else:
                st.warning("분석을 위한 충분한 기간의 데이터가 확보되지 않았습니다.")
        else:
            st.error("데이터를 가져오는 데 실패했습니다. 품목명을 다시 확인해 주세요.")
