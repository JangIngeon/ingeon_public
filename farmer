import streamlit as st
import pandas as pd

st.title('🛒 Fresh Up - 업사이클링 농산물 판매')

# 1️⃣ 저품질 농산물 필터링 (3등급 이하)
def filter_low_quality(rating):
    low_quality = rating[rating['등급'].str.contains('보통|3등')]
    return low_quality

# 2️⃣ 소비자 수요 높은 품목 선정 (Trend 데이터 활용)
def get_top_trending_items(trend, top_n=5):
    top_items = trend.groupby('품목')['판매금액(원)'].sum().nlargest(top_n).index
    return top_items

# 3️⃣ 저품질 상위 품목 필터링
def filter_low_quality_top_items(rating, top_items):
    low_quality = filter_low_quality(rating)
    filtered = low_quality[low_quality['품목명'].isin(top_items)]
    return filtered

# 4️⃣ 농가 매칭 (Farmer 데이터 활용)
def match_farmers(farmer, products):
    matched_farmers = farmer[farmer['품목'].isin(products)]
    return matched_farmers

# 5️⃣ 소비자 구매 페이지 (최종 업사이클링 상품 제공)
def display_products(low_quality_df):
    st.subheader('🛒 구매 가능한 업사이클링 제품:')
    for _, row in low_quality_df.iterrows():
        st.write(f"- {row['품목명']} ({row['등급']}): {row['가격']}원 (산지: {row['산지']})")

# 데이터 로드 (이미 로드된 trend, rating, farmer 사용)
trend = pd.read_csv('trend.csv')
rating = pd.read_csv('rating.csv')
farmer = pd.read_csv('farmer.csv')

# 실행
st.subheader('🔥 상위 소비자 수요 품목 선정')
top_n = st.slider('상위 N개 품목', min_value=1, max_value=10, value=5)
top_items = get_top_trending_items(trend, top_n)
st.write(f'선정된 품목: {list(top_items)}')

low_quality_top = filter_low_quality_top_items(rating, top_items)
st.subheader('📉 저품질 상위 품목')
st.write(low_quality_top)

matched_farmers = match_farmers(farmer, low_quality_top['품목명'].unique())
st.subheader('🏡 매칭된 농가')
st.write(matched_farmers)

st.subheader('🛒 소비자 구매 페이지')
display_products(low_quality_top)
