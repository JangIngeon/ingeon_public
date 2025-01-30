import streamlit as st

# 이름 입력 받기
name = st.text_input("이름을 입력하세요:")

# 확인 버튼
if st.button("확인"):
    if name:
        # 텍스트와 이미지 함께 출력
        st.markdown(f"""
        <h1 style='color: red; font-size: 60px; text-align: center;'>쉬나 받으십쇼</h1>
        <img src="https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/cnoC/image/-z3AZcHOGwkI_TnqZmiLn3kvzyQ" alt="Image" style="display: block; margin: 0 auto; width: 50%;">
        """, unsafe_allow_html=True)
    else:
        st.write("이름을 입력해주세요.")



