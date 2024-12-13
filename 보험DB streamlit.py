import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# MySQL 연결 함수
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",  # MySQL 서버 주소
        user="root",       # 사용자 계정
        password="1234",   # 비밀번호
        db="Insu",  # 데이터베이스 이름
        charset="utf8"
    )

# SQL 실행 함수
def fetch_data(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# Streamlit 앱
st.title("보험 DB 조회 및 분석")

# SQL 쿼리 입력
query = st.text_area("SQL 쿼리를 입력하세요", "SELECT * FROM customers LIMIT 10")

# 쿼리 실행 버튼
if st.button("쿼리 실행"):
    try:
        # 데이터 조회
        data = fetch_data(query)
        st.write("데이터 조회 성공!")
        st.dataframe(data)

        # 데이터 분석 예제
        if 'gender' in data.columns:
            st.subheader("성별 비율 분석")
            gender_count = data['gender'].value_counts()
            fig = px.pie(values=gender_count, names=gender_count.index, title="성별 비율")
            st.plotly_chart(fig)
    except Exception as e:
        st.error(f"오류 발생: {e}")

