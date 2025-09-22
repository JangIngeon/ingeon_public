# app.py
import streamlit as st
from datetime import date

st.set_page_config(page_title="연애일지 💕", page_icon="💌", layout="centered")

st.title("연애 기록 ❤️")

# 입력 칸
your_name = st.text_input("본인 이름")
partner_name = st.text_input("남자친구 이름")
start_date = st.date_input("사귀기로 한 날짜", value=date.today())

# 버튼
if st.button("확인하기 💌"):
    today = date.today()
    days = (today - start_date).days + 1

    if days <= 0:
        st.error("❌ 시작일이 오늘 이후예요. 올바른 날짜를 선택해주세요.")
    else:
        # 성 빼고 이름만 추출
        short_name = your_name[1:] if len(your_name) > 1 else your_name

        # 결과 출력
        st.markdown("<div style='text-align:center; padding:20px'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin:10px'>{your_name} ♥ {partner_name}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:10px'>사귄지 {days}일째에요~</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:10px'>{short_name}아 사랑해 💕</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


