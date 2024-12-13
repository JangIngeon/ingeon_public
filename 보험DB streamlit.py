import streamlit as st
import pandas as pd
import pymysql
import duckdb

# MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        user='root',
        passwd='1234',
        host='127.0.0.1',
        db='Insu',
        charset='utf8'
    )

# MySQL에 쿼리하고 결과를 pandas DataFrame으로 반환
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

# Streamlit 앱 구성
st.title("보험 DB 조회 및 분석")

# 사용자 입력 - SQL 쿼리 입력
query = st.text_area("SQL 쿼리를 입력하세요", "SELECT * FROM customers LIMIT 10")

# SQL 실행 버튼
if st.button("쿼리 실행"):
    if query.strip():
        try:
            # SQL 실행 및 결과 출력
            data = sqldf(query)
            if not data.empty:
                st.success("데이터 조회 성공!")
                st.dataframe(data)  # DataFrame을 테이블로 출력
            else:
                st.warning("결과가 없습니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.warning("SQL 쿼리를 입력하세요.")

# 데이터 분석 - 예제: 고객 수 통계
st.header("고객 통계 분석")
if st.button("고객 수 분석 실행"):
    try:
        stats_query = "SELECT COUNT(*) AS customer_count FROM customers"
        stats_data = sqldf(stats_query)
        st.write("고객 수:", stats_data.iloc[0]['customer_count'])
    except Exception as e:
        st.error(f"분석 중 오류 발생: {e}")


