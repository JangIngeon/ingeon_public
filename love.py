# save as app.py and run: streamlit run app.py
import streamlit as st
from datetime import date, datetime

st.set_page_config(page_title="연애일지 ❤️", page_icon="💌", layout="centered")

st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
st.markdown("<h1 style='margin:0'>본인 ♥ 남자친구</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.write("---")

# 입력
col1, col2 = st.columns(2)
with col1:
    your_name = st.text_input("본인 이름", value="")
with col2:
    partner_name = st.text_input("남자친구 이름", value="")

start_date = st.date_input("사귀기로 한 날짜", value=date.today())

# 계산 (한국식: 사귄 첫날을 1일째로 셈)
today = date.today()
delta_days = (today - start_date).days + 1
if delta_days <= 0:
    st.warning("시작일이 미래입니다. 올바른 날짜를 선택해주세요.")
else:
    # 크게 보이게 출력
    st.markdown("<div style='text-align:center; padding:18px'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='margin:6px'>{your_name} ♥ {partner_name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='margin:6px; font-size:46px'>{delta_days}일째에요~</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin-top:12px; font-size:28px'>({partner_name})아 사랑해~ 💕</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 메시지 텍스트 생성 및 다운로드 버튼
    message = f"{your_name} ♥ {partner_name}\n사귄지 {delta_days}일째에요~\n({partner_name})아 사랑해~\n(기념일: {start_date.isoformat()})"
    st.download_button("메시지 텍스트 다운로드", data=message, file_name="love_message.txt", mime="text/plain")

# 간단한 스타일/배경 옵션 (선택)
st.write("---")
with st.expander("디자인 옵션 (선택)"):
    st.info("여기에서 색, 이모지, 출력 문구 등을 더 바꿀 수 있도록 확장해보세요.")
    st.caption("원하시면 이 코드에 배경이미지, 공유 버튼, 카드 이미지로 변환하는 기능 등도 추가해 드려요.")
