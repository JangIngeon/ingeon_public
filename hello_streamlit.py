import streamlit as st

# 이름 입력 받기
name = st.text_input("이름을 입력하세요:")

# 입력한 이름이 있으면 메시지 출력
if name:
    st.write(f"{name}은/는 바보입니다")
