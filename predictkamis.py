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

# 1. SSL 보안 설정 강제 완화 (Handshake Failure 해결 핵심)
class LegacyPrefixAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1') # 보안 등급을 낮춰 구형 서버 접속 허용
        kwargs['ssl_context'] = context
        return super(LegacyPrefixAdapter, self).init_poolmanager(*args, **kwargs)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 2. KAMIS API 실시간 데이터 수집 함수 ---
def get_kamis_data(item_name, start_date="2024-01-01"):
    end_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # 코드표 로드
        df_map = pd.read_csv('농축수산물 품목 및 등급 코드표.csv')
        target = df_map[df_map['품목명'] == item_name].iloc[0]
        
        c_code = str(int(target['품목 그룹코드']))
        i_code = str(int(target['품목 코드']))
        k_code = str(int(target['품종코드'])).zfill(2)

        # API 호출 설정
        url = "https://www.kamis.or.kr/service/price/xml.do"
        params = {
            "action": "periodProductList",
            "p_cert_key": "31f6d529-1b15-407d-a46c-bce8afdad18c",
            "p_cert_id": "5652",
            "p_returntype": "xml",
            "p_startday": start_date,
            "p_endday": end_date,
            "p_productclscode": "02",
            "p_itemcategorycode": c_code,
            "p_itemcode": i_code,
            "p_kindcode": k_code,
            "p_productrankcode": "04",
            "p_countrycode": "1101",
            "p_convert_kg_yn": "Y"
        }

        # 세션을 생성하고 어댑터 적용 (Handshake 오류 방지)
        session = requests.Session()
        session.mount("https://", LegacyPrefixAdapter())
        
        # verify=False와 함께 요청
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
                    "가격(1kg)": int(p_text)
                })
        
        res_df = pd.DataFrame(data_list)
        if not res_df.empty:
            res_df['날짜'] = pd.to_datetime(res_df['날짜'])
            return res_df.sort_values('날짜')
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"데이터 수집 중 상세 오류: {e}")
        return pd.DataFrame()

# (이하 분석 및 UI 로직은 이전과 동일)
# ... [생략] ...

st.title("🥬 실시간 가격 예측 서비스 (SSL 오류 수정판)")
# (중략) 사이드바 및 버튼 로직 적용
