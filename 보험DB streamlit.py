# 필수 라이브러리 임포트
import pymysql
import pandas as pd
import duckdb  # pip install duckdb

# MySQL 연결 설정
dbConn = pymysql.connect(
    user='root',           # 사용자 이름
    passwd='1234',         # 비밀번호
    host='127.0.0.1',      # MySQL 서버 주소
    db='Insu',             # 데이터베이스 이름
    charset='utf8'         # 문자 인코딩
)
cursor = dbConn.cursor(pymysql.cursors.DictCursor)

# MySQL에 쿼리하고 결과를 DataFrame으로 반환
def sqldf(sql):
    """
    MySQL에 쿼리를 실행하고 결과를 pandas DataFrame으로 반환합니다.
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# MySQL에 쿼리하고 결과를 딕셔너리로 반환
def sqldic(sql):
    """
    MySQL에 쿼리를 실행하고 결과를 딕셔너리로 반환합니다.
    """
    cursor.execute(sql)
    return cursor.fetchall()

# DuckDB로 쿼리 실행 후 DataFrame 반환
def dfsql(query):
    """
    DuckDB를 사용해 쿼리를 실행하고 결과를 pandas DataFrame으로 반환합니다.
    """
    return duckdb.query(query).df()
