import streamlit as st
import pymysql
import pandas as pd

# MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        user='root',       # MySQL 사용자명
        passwd='1234',     # MySQL 비밀번호
        host='127.0.0.1',  # 로컬호스트
        db='Insu',         # 데이터베이스 이름
        charset='utf8'     # 문자셋
    )

# MySQL 쿼리 실행 및 결과를 DataFrame으로 반환
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

# Streamlit 애플리케이션
st.title("보험 데이터베이스 분석 도구")
st.markdown("**`Insu` 데이터베이스와 연결하여 SQL 쿼리를 실행합니다.**")

# SQL 입력 텍스트 박스
query = st.text_area("쿼리를 입력하세요", 
                     '''SELECT AGE, SEX FROM cust LIMIT 10''')

# 실행 버튼
if st.button("쿼리 실행"):
    if query.strip():  # SQL 쿼리가 비어 있지 않은 경우
        try:
            df = sqldf(query)
            if not df.empty:
                st.success("쿼리 실행 성공!")
                st.write("**결과 데이터프레임:**")
                st.dataframe(df)  # 데이터프레임을 웹페이지에 표시
            else:
                st.warning("결과가 없습니다. 쿼리를 확인하세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.warning("SQL 쿼리를 입력하세요.")

# 도움말
st.markdown("""
---
### 사용 방법:
1. SQL 쿼리를 입력하고 **쿼리 실행** 버튼을 클릭하세요.
2. 데이터베이스 테이블에서 원하는 데이터를 가져옵니다.
3. 결과는 데이터프레임 형태로 표시됩니다.
""")



