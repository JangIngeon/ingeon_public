import streamlit as st
import pymysql
import pandas as pd

# MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        user='root',  # 사용자명
        passwd='1234',  # 비밀번호
        host='127.0.0.1',  # 로컬 서버
        db='Insu',  # 데이터베이스 이름
        charset='utf8'  # 문자셋
    )

# SQL 실행 및 DataFrame 반환
def execute_query(sql):
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

# Streamlit 애플리케이션 시작
st.title("보험 데이터베이스 조회 및 분석")
st.markdown("**`Insu` 데이터베이스와 연결된 SQL 쿼리 인터페이스입니다.**")

# 사용자 SQL 입력
query = st.text_area("SQL 쿼리를 입력하세요", "SELECT * FROM customers LIMIT 10")

# SQL 실행 버튼
if st.button("쿼리 실행"):
    if query.strip():  # 쿼리가 비어있지 않은 경우
        try:
            data = execute_query(query)
            if not data.empty:
                st.success("쿼리 실행 성공!")
                st.dataframe(data)  # DataFrame 결과를 테이블로 출력
            else:
                st.warning("쿼리 결과가 없습니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.warning("SQL 쿼리를 입력하세요.")

# 기타 정보
st.markdown("""
---
#### 사용 방법
1. SQL 쿼리를 입력합니다.
2. 실행 결과는 테이블 형식으로 표시됩니다.
3. 필요한 데이터 분석이나 조회 작업을 직접 수행하세요.
""")

