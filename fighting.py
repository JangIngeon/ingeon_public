import streamlit as st

# 이름 입력 받기
name = st.text_input("이름을 입력하세요:")

# 확인 버튼
if st.button("확인"):
    if name:
        # 성을 제외한 이름 부분 추출
        first_name = name[1:]  # 첫 글자를 제외한 나머지
        
        # 파란색 글씨로 출력
        st.markdown(f"""
        <h1 style='color: #1E90FF; font-family: "Comic Sans MS", cursive, sans-serif; font-size: 60px; text-align: center;'> 
        {first_name}아 힘내!</h1>
        """, unsafe_allow_html=True)
    else:
        st.write("이름을 입력해주세요.")
