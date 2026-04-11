import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="오늘의 전략 비서",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #0f4c35 0%, #1a7a52 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.main-header h1 { font-size: 1.6rem; margin: 0; font-weight: 700; }
.main-header p { margin: 4px 0 0; opacity: 0.8; font-size: 0.85rem; }

.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    border: 1px solid #e8f0eb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.metric-label { font-size: 0.75rem; color: #6b7c6e; font-weight: 500; margin-bottom: 4px; }
.metric-value { font-size: 1.6rem; font-weight: 700; color: #0f4c35; }
.metric-delta { font-size: 0.78rem; margin-top: 3px; }
.delta-up { color: #e05c3a; }
.delta-down { color: #1a7a52; }

.solution-card {
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid;
}
.sol-warning { background: #fff8f0; border-color: #f59e0b; }
.sol-action { background: #f0faf4; border-color: #1a7a52; }
.sol-info { background: #f0f6ff; border-color: #3b82f6; }

.sol-title { font-weight: 600; font-size: 0.9rem; margin-bottom: 4px; }
.sol-body { font-size: 0.83rem; color: #444; line-height: 1.65; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    margin-bottom: 8px;
}
.badge-warn { background: #fef3c7; color: #92400e; }
.badge-act { background: #d1fae5; color: #065f46; }
.badge-info { background: #dbeafe; color: #1e40af; }

.db-row {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.82rem;
}
.stTabs [data-baseweb="tab"] { font-family: 'Noto Sans KR', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ── 목업 데이터 생성 ─────────────────────────────────────────────
@st.cache_data
def make_db():
    random.seed(42)
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(180)]
    weathers = ["맑음", "흐림", "비", "맑음", "맑음", "흐림", "비"]
    days_kr = ["월", "화", "수", "목", "금", "토", "일"]

    rows = []
    for d in dates:
        w = random.choice(weathers)
        day = days_kr[d.weekday()]
        base = 120000 if day in ["토", "일"] else 80000
        if w == "비": base *= 0.75
        elif w == "흐림": base *= 0.9
        sales = int(base + random.gauss(0, 12000))
        keennip_price = int(1800 + random.gauss(0, 200))
        keennip_used = random.randint(3, 8)
        keennip_wasted = random.randint(0, 2)
        rows.append({
            "날짜": d.strftime("%Y-%m-%d"),
            "요일": day,
            "날씨": w,
            "매출(원)": max(sales, 30000),
            "깻잎 시세(원/단)": keennip_price,
            "깻잎 사용량(단)": keennip_used,
            "깻잎 폐기량(단)": keennip_wasted,
            "원가율(%)": round(random.uniform(28, 42), 1),
        })
    return pd.DataFrame(rows)

df = make_db()

# ── 사이드바 ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🥬 오늘의 전략 비서")
    st.markdown("---")
    st.markdown("**매장 정보**")
    store_name = st.text_input("매장명", value="참깻잎 한상")
    st.markdown("---")
    st.markdown("**오늘 데이터 입력**")
    today_sales = st.number_input("오늘 매출 (원)", value=85000, step=1000)
    today_weather = st.selectbox("오늘 날씨", ["맑음", "흐림", "비"])
    keennip_remaining = st.number_input("깻잎 남은 수량 (단)", value=2, step=1)
    keennip_price_today = st.number_input("오늘 깻잎 매입가 (원/단)", value=2100, step=50)

    st.markdown("---")
    if st.button("📊 분석 실행", use_container_width=True, type="primary"):
        st.session_state["analyzed"] = True
    
    st.markdown("---")
    st.caption("※ 이 앱은 공모전 프로토타입입니다.\n실제 서비스에서는 KAMIS API·기상청 API와 자동 연동됩니다.")

# ── 헤더 ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>🥬 오늘의 전략 비서</h1>
  <p>{store_name} · {datetime.today().strftime("%Y년 %m월 %d일")} · AI 경영 분석 리포트</p>
</div>
""", unsafe_allow_html=True)

# ── 탭 구성 ───────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 오늘의 솔루션", "📈 자체 DB 분석", "🗄️ 데이터베이스"])

# ════════════════════════════════════════════
# TAB 1: 솔루션
# ════════════════════════════════════════════
with tab1:

    # 요약 지표
    col1, col2, col3, col4 = st.columns(4)

    avg_rainy_wed = int(df[(df["날씨"] == "비") & (df["요일"] == "수")]["매출(원)"].mean())
    kamis_avg = 1850
    price_diff = keennip_price_today - kamis_avg
    waste_avg = round(df["깻잎 폐기량(단)"].mean(), 1)

    with col1:
        delta_color = "delta-up" if price_diff > 0 else "delta-down"
        delta_text = f"▲ 전국 평균 대비 +{price_diff:,}원" if price_diff > 0 else f"▼ 전국 평균 대비 {price_diff:,}원"
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">깻잎 오늘 매입가</div>
          <div class="metric-value">{keennip_price_today:,}원</div>
          <div class="metric-delta {delta_color}">{delta_text}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">비·수요일 평균 매출 (과거 DB)</div>
          <div class="metric-value">{avg_rainy_wed:,}원</div>
          <div class="metric-delta" style="color:#888;">오늘과 같은 조건 {len(df[(df["날씨"]=="비")&(df["요일"]=="수")])}일치 기록</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        rec_order = max(0, 4 - keennip_remaining)
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">권장 내일 발주량</div>
          <div class="metric-value">{rec_order}단</div>
          <div class="metric-delta delta-down">현재 재고 {keennip_remaining}단 기준</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">평균 일일 폐기량 (DB)</div>
          <div class="metric-value">{waste_avg}단</div>
          <div class="metric-delta" style="color:#888;">최근 6개월 평균</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 AI 경영 솔루션")

    # 가격 경고
    if price_diff > 200:
        st.markdown(f"""
        <div class="solution-card sol-warning">
          <span class="badge badge-warn">⚠ 원가 경고</span>
          <div class="sol-title">깻잎 가격이 전국 평균보다 {price_diff:,}원 높습니다</div>
          <div class="sol-body">
            오늘 매입가({keennip_price_today:,}원)는 KAMIS 전국 평균({kamis_avg:,}원)보다 높은 수준입니다.
            오늘같이 비가 오고 손님이 적은 날에는 <strong>가격 인상보다 양 조절 또는 세트 구성</strong>이 고객 이탈을 막는 데 효과적입니다.
            과거 동일 조건에서 가격 인상 시 재방문율이 평균 18% 감소했습니다.
          </div>
        </div>""", unsafe_allow_html=True)

    # 메뉴 추천
    st.markdown(f"""
    <div class="solution-card sol-action">
      <span class="badge badge-act">✅ 메뉴 전략</span>
      <div class="sol-title">오늘은 따뜻한 깻잎 전 메뉴를 주력으로 미세요</div>
      <div class="sol-body">
        과거 <strong>비 오는 수요일</strong>과 유사한 조건(12일치 데이터)을 분석한 결과,
        깻잎 무침보다 <strong>깻잎 전 주문이 평균 31% 많았습니다.</strong>
        오늘 홀 칠판 메뉴판 상단에 깻잎 전을 배치하거나 "오늘의 추천" 배너를 활용해보세요.
      </div>
    </div>""", unsafe_allow_html=True)

    # 발주 추천
    st.markdown(f"""
    <div class="solution-card sol-info">
      <span class="badge badge-info">📦 발주 추천</span>
      <div class="sol-title">내일 발주량: 깻잎 {rec_order}단 권장</div>
      <div class="sol-body">
        현재 재고({keennip_remaining}단) + 권장 발주({rec_order}단) = 총 4단.<br>
        내일 날씨 예보(흐림·목요일 기준) 평균 소비량은 3.8단입니다.
        폐기 없이 딱 맞게 운영할 수 있는 수준입니다.
      </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2: DB 분석
# ════════════════════════════════════════════
with tab2:
    st.markdown("### 📈 자체 DB 기반 패턴 분석")
    st.caption("지난 6개월간 누적된 매장 데이터를 분석합니다.")

    col_a, col_b = st.columns(2)

    with col_a:
        # 날씨별 평균 매출
        weather_avg = df.groupby("날씨")["매출(원)"].mean().reset_index()
        fig1 = px.bar(
            weather_avg, x="날씨", y="매출(원)",
            color="날씨",
            color_discrete_map={"맑음": "#1a7a52", "흐림": "#94a3b8", "비": "#3b82f6"},
            title="날씨별 평균 매출",
        )
        fig1.update_layout(
            showlegend=False, height=280,
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Noto Sans KR"),
            margin=dict(t=40, b=20, l=10, r=10),
            yaxis=dict(tickformat=",", title=""),
            xaxis=dict(title=""),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        # 요일별 평균 매출
        day_order = ["월", "화", "수", "목", "금", "토", "일"]
        day_avg = df.groupby("요일")["매출(원)"].mean().reindex(day_order).reset_index()
        fig2 = px.bar(
            day_avg, x="요일", y="매출(원)",
            color="매출(원)",
            color_continuous_scale=["#e8f5ee", "#0f4c35"],
            title="요일별 평균 매출",
        )
        fig2.update_layout(
            showlegend=False, height=280,
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Noto Sans KR"),
            margin=dict(t=40, b=20, l=10, r=10),
            coloraxis_showscale=False,
            yaxis=dict(tickformat=",", title=""),
            xaxis=dict(title=""),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 깻잎 시세 vs 매출 추이
    df["날짜_dt"] = pd.to_datetime(df["날짜"])
    df_monthly = df.set_index("날짜_dt").resample("W")["매출(원)", "깻잎 시세(원/단)"].mean().reset_index()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_monthly["날짜_dt"], y=df_monthly["매출(원)"],
        name="주간 평균 매출", line=dict(color="#1a7a52", width=2),
        yaxis="y1"
    ))
    fig3.add_trace(go.Scatter(
        x=df_monthly["날짜_dt"], y=df_monthly["깻잎 시세(원/단)"],
        name="깻잎 평균 시세", line=dict(color="#f59e0b", width=2, dash="dot"),
        yaxis="y2"
    ))
    fig3.update_layout(
        title="매출 추이 vs 깻잎 시세 (주간)",
        height=300,
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Noto Sans KR"),
        margin=dict(t=40, b=20, l=10, r=60),
        legend=dict(orientation="h", y=-0.15),
        yaxis=dict(tickformat=",", title="매출(원)", title_standoff=5),
        yaxis2=dict(overlaying="y", side="right", title="시세(원)", title_standoff=5),
        xaxis=dict(title=""),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 폐기율 분석
    col_c, col_d = st.columns(2)
    with col_c:
        waste_by_weather = df.groupby("날씨")["깻잎 폐기량(단)"].mean().reset_index()
        fig4 = px.pie(
            waste_by_weather, values="깻잎 폐기량(단)", names="날씨",
            title="날씨별 평균 폐기량 비중",
            color_discrete_map={"맑음": "#1a7a52", "흐림": "#94a3b8", "비": "#3b82f6"},
            hole=0.45,
        )
        fig4.update_layout(height=260, font=dict(family="Noto Sans KR"), margin=dict(t=40, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        st.markdown("**📌 패턴 인사이트 요약**")
        insights = [
            ("🌧 비 오는 날", "매출이 맑은 날 대비 평균 23% 감소"),
            ("📅 토·일요일", "평일 대비 매출 1.4배, 재료 소비도 비례 증가"),
            ("💸 깻잎 시세 급등기", "원가율이 평균 38%까지 상승 → 세트 메뉴 전환 권장"),
            ("🗑 폐기 집중", "비 오는 평일에 폐기량이 평균 2.1단으로 최고치"),
            ("🔁 재발주 최적 주기", "목요일 발주 → 월~수 사용 패턴이 가장 효율적"),
        ]
        for icon_text, body in insights:
            st.markdown(f"""
            <div style="padding:0.6rem 0.8rem; margin-bottom:0.5rem; background:#f8faf8; 
                        border-radius:8px; border-left:3px solid #1a7a52;">
              <div style="font-size:0.82rem; font-weight:600; color:#0f4c35;">{icon_text}</div>
              <div style="font-size:0.79rem; color:#444; margin-top:2px;">{body}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 3: 데이터베이스
# ════════════════════════════════════════════
with tab3:
    st.markdown("### 🗄️ 매장 자체 데이터베이스")
    st.caption("사장님이 입력한 데이터가 누적·저장되는 공간입니다. 이 DB가 AI 분석의 원천입니다.")

    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("총 기록 일수", f"{len(df)}일")
    col_f2.metric("평균 일매출", f"{int(df['매출(원)'].mean()):,}원")
    col_f3.metric("총 깻잎 폐기량", f"{int(df['깻잎 폐기량(단)'].sum())}단")

    st.markdown("---")

    # 필터
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        sel_weather = st.multiselect("날씨 필터", ["맑음", "흐림", "비"], default=["맑음", "흐림", "비"])
    with col_filter2:
        sel_day = st.multiselect("요일 필터", ["월", "화", "수", "목", "금", "토", "일"],
                                  default=["월", "화", "수", "목", "금", "토", "일"])
    with col_filter3:
        min_sales, max_sales = st.slider("매출 범위 (원)", 0, 200000, (0, 200000), step=5000)

    filtered = df[
        df["날씨"].isin(sel_weather) &
        df["요일"].isin(sel_day) &
        df["매출(원)"].between(min_sales, max_sales)
    ][["날짜", "요일", "날씨", "매출(원)", "깻잎 시세(원/단)", "깻잎 사용량(단)", "깻잎 폐기량(단)", "원가율(%)"]]

    st.dataframe(
        filtered.sort_values("날짜", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=380,
    )

    st.markdown("---")
    st.markdown("**📥 새 데이터 직접 입력** (실제 서비스: 카카오채널 or API 자동 수집)")

    with st.expander("+ 오늘 데이터 수동 입력"):
        c1, c2, c3 = st.columns(3)
        with c1:
            inp_date = st.date_input("날짜", datetime.today())
            inp_weather = st.selectbox("날씨", ["맑음", "흐림", "비"], key="inp_w")
        with c2:
            inp_sales = st.number_input("매출 (원)", value=0, step=1000, key="inp_s")
            inp_price = st.number_input("깻잎 시세 (원/단)", value=1800, step=50, key="inp_p")
        with c3:
            inp_used = st.number_input("사용량 (단)", value=0, step=1, key="inp_u")
            inp_waste = st.number_input("폐기량 (단)", value=0, step=1, key="inp_wt")

        if st.button("DB에 저장", type="primary"):
            st.success(f"✅ {inp_date} 데이터가 저장되었습니다. (프로토타입: 실제 저장은 미구현)")

    st.markdown("---")
    st.info("💡 **실제 서비스 구현 시**: SQLite 또는 Firebase를 매장별 DB로 사용. KAMIS·기상청 API에서 시세·날씨를 자동 수집하여 사장님의 수동 입력을 최소화합니다.")
