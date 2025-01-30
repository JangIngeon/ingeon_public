import streamlit as st

# 이름 입력 받기
name = st.text_input("이름을 입력하세요:")

# 확인 버튼
if st.button("확인"):
    if name:
        st.markdown(f"<h1 style='color: red; font-size: 60px; text-align: center;'>당신은 바보입니다</h1>", unsafe_allow_html=True)
    else:
        st.write("이름을 입력해주세요.")

