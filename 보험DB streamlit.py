# app.py
import streamlit as st
import pandas as pd
import pymysql

# MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        user='root',
        passwd='1234',
        host='127.0.0.1',
        db='Insu',
        charset='utf8'
    )

# SQL 실행 및 DataFrame 반환
def sqldf(sql):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return pd.DataFrame(result)
    except Exception as e:
        st.error(f"SQL 실행 오류: {e}")
        return pd.DataFrame()

# Streamlit 앱
st.title("보험 DB 조회 및 분석")

# SQL 입력
query = st.text_area("SQL 쿼리를 입력하세요", "SELECT * FROM customers LIMIT 10")

if st.button("쿼리 실행"):
    if query.strip():
        data = sqldf(query)
        if not data.empty:
            st.success("데이터 조회 성공!")
            st.dataframe(data)
        else:
            st.warning("결과가 없습니다.")
    else:
        st.warning("SQL 쿼리를 입력하세요.")
