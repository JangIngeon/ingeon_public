import pymysql
import pandas as pd
import duckdb # pip install duckdb
dbConn = pymysql.connect(user='root', passwd='1234', host='127.0.0.1', db='Insu', charset='utf8')
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

# MySQL에 쿼리하고 결과를 dataframe으로 반환
def sqldf(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# MySQL에 쿼리하고 결과를 딕셔너리로 반환
def sqldic(sql):
    cursor.execute(sql)
    return cursor.fetchall()

# 데이터프레임에 쿼리한 결과를 데이터프레임으로 반환
def dfsql(query):
   return duckdb.query(query).df()

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


