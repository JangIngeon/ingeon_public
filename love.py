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

        # 말풍선 스타일 CSS
        bubble_style = """
        <style>
        .bubble {
            display: inline-block;
            background: #ffe6f0;
            color: #333;
            padding: 20px 30px;
            border-radius: 25px;
            font-size: 20px;
            line-height: 1.6;
            position: relative;
            box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        }
        .bubble::after {
            content: '';
            position: absolute;
            bottom: -20px;
            left: 40px;
            border-width: 20px 15px 0;
            border-style: solid;
            border-color: #ffe6f0 transparent transparent transparent;
        }
        </style>
        """

        # 결과 출력
        st.markdown(bubble_style, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='text-align:center; margin-top:30px'>
                <h1>{your_name} 💖 {partner_name}</h1>
                <div class="bubble">
                    사귄지 <b>{days}일째</b>에요~ <br>
                    {short_name}아 사랑해 💕
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )



