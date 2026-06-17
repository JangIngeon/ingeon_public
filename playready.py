# -*- coding: utf-8 -*-
"""
Play Ready — AI 기반 통합 컨디션 관리 플랫폼 (데모)
실행: pip install streamlit pandas numpy plotly
      streamlit run play_ready_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------
st.set_page_config(page_title="Play Ready", page_icon="⚽", layout="wide")

PRIMARY = "#6D28D9"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
RED = "#DC2626"

BODY_PARTS = ["없음", "발목", "무릎", "햄스트링", "허벅지", "종아리", "허리", "어깨", "손목"]
POSITIONS = ["GK", "DF", "MF", "FW"]

# ----------------------------------------------------------------------
# 3D 인체 모형 (스켈레톤) 좌표 — Body Ready 통증 부위 시각화용
# ----------------------------------------------------------------------
BODY_POINTS = {
    "head": (0, 0, 9.3, 24),
    "neck": (0, 0, 8.5, 10),
    "chest": (0, 0, 7.2, 20),
    "shoulder_L": (-1.3, 0.0, 7.9, 14),
    "shoulder_R": (1.3, 0.0, 7.9, 14),
    "elbow_L": (-1.7, 0.3, 6.2, 10),
    "elbow_R": (1.7, 0.3, 6.2, 10),
    "wrist_L": (-1.9, 0.5, 4.5, 11),
    "wrist_R": (1.9, 0.5, 4.5, 11),
    "waist": (0, 0, 5.5, 18),
    "hip_L": (-0.6, 0, 5.0, 12),
    "hip_R": (0.6, 0, 5.0, 12),
    "thigh_L": (-0.6, 0, 3.4, 13),
    "thigh_R": (0.6, 0, 3.4, 13),
    "hamstring_L": (-0.6, 0.55, 2.8, 12),
    "hamstring_R": (0.6, 0.55, 2.8, 12),
    "knee_L": (-0.6, 0, 1.9, 10),
    "knee_R": (0.6, 0, 1.9, 10),
    "calf_L": (-0.6, 0, 1.0, 11),
    "calf_R": (0.6, 0, 1.0, 11),
    "ankle_L": (-0.6, 0, 0.2, 9),
    "ankle_R": (0.6, 0, 0.2, 9),
}

BODY_EDGES = [
    ("head", "neck"), ("neck", "chest"),
    ("chest", "shoulder_L"), ("chest", "shoulder_R"),
    ("shoulder_L", "elbow_L"), ("elbow_L", "wrist_L"),
    ("shoulder_R", "elbow_R"), ("elbow_R", "wrist_R"),
    ("chest", "waist"), ("waist", "hip_L"), ("waist", "hip_R"),
    ("hip_L", "thigh_L"), ("thigh_L", "hamstring_L"), ("hamstring_L", "knee_L"),
    ("knee_L", "calf_L"), ("calf_L", "ankle_L"),
    ("hip_R", "thigh_R"), ("thigh_R", "hamstring_R"), ("hamstring_R", "knee_R"),
    ("knee_R", "calf_R"), ("calf_R", "ankle_R"),
]

PART_TO_NODES = {
    "어깨": ["shoulder_L", "shoulder_R"],
    "손목": ["wrist_L", "wrist_R"],
    "허리": ["waist"],
    "허벅지": ["thigh_L", "thigh_R"],
    "햄스트링": ["hamstring_L", "hamstring_R"],
    "무릎": ["knee_L", "knee_R"],
    "종아리": ["calf_L", "calf_R"],
    "발목": ["ankle_L", "ankle_R"],
}

NODE_LABELS_KR = {
    "head": "머리", "neck": "목", "chest": "가슴",
    "shoulder_L": "어깨(좌)", "shoulder_R": "어깨(우)",
    "elbow_L": "팔꿈치(좌)", "elbow_R": "팔꿈치(우)",
    "wrist_L": "손목(좌)", "wrist_R": "손목(우)",
    "waist": "허리", "hip_L": "골반(좌)", "hip_R": "골반(우)",
    "thigh_L": "허벅지(좌)", "thigh_R": "허벅지(우)",
    "hamstring_L": "햄스트링(좌)", "hamstring_R": "햄스트링(우)",
    "knee_L": "무릎(좌)", "knee_R": "무릎(우)",
    "calf_L": "종아리(좌)", "calf_R": "종아리(우)",
    "ankle_L": "발목(좌)", "ankle_R": "발목(우)",
}


def build_body_figure(pain_area, pain_level=0):
    """선택된 통증 부위를 강조한 3D 인체 스켈레톤 모형을 생성한다."""
    highlighted = set(PART_TO_NODES.get(pain_area, []))

    # 뼈대(연결선)
    edge_x, edge_y, edge_z = [], [], []
    for a, b in BODY_EDGES:
        xa, ya, za, _ = BODY_POINTS[a]
        xb, yb, zb, _ = BODY_POINTS[b]
        edge_x += [xa, xb, None]
        edge_y += [ya, yb, None]
        edge_z += [za, zb, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z, mode="lines",
        line=dict(color="#9CA3AF", width=14),
        hoverinfo="skip", showlegend=False,
    ))

    # 관절/부위 마커
    node_names = list(BODY_POINTS.keys())
    xs = [BODY_POINTS[n][0] for n in node_names]
    ys = [BODY_POINTS[n][1] for n in node_names]
    zs = [BODY_POINTS[n][2] for n in node_names]
    sizes = [BODY_POINTS[n][3] + (6 if n in highlighted else 0) for n in node_names]
    colors = [RED if n in highlighted else "#E5E7EB" for n in node_names]
    line_colors = [RED if n in highlighted else "#9CA3AF" for n in node_names]
    hover_text = [
        f"{NODE_LABELS_KR[n]}" + (f" · 통증 강도 {pain_level}/10" if n in highlighted else "")
        for n in node_names
    ]

    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs, mode="markers",
        marker=dict(size=sizes, color=colors, line=dict(width=2, color=line_colors), opacity=0.95),
        text=hover_text, hoverinfo="text", showlegend=False,
    ))

    fig.update_layout(
        height=460,
        margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(
            xaxis=dict(visible=False, range=[-3, 3]),
            yaxis=dict(visible=False, range=[-2, 2]),
            zaxis=dict(visible=False, range=[-0.5, 10]),
            aspectmode="manual",
            aspectratio=dict(x=0.8, y=0.6, z=1.6),
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.7)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig

st.markdown(
    f"""
    <style>
    .pr-badge {{
        display:inline-block; padding:2px 10px; border-radius:12px;
        font-size:0.8rem; font-weight:600; color:white;
    }}
    .pr-card {{
        border-radius:14px; padding:18px 16px; text-align:center;
        border:1px solid #eee;
    }}
    h1, h2, h3 {{ color: #1f2937; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# 데이터 생성 / 계산 로직
# ----------------------------------------------------------------------
def compute_readiness(row):
    score = 100.0
    score -= row["fatigue"] * 3
    score -= row["pain_level"] * 4
    score -= max(0, row["rpe"] - 7) * 2
    score += (row["sleep_score"] - 70) * 0.2
    score -= max(0, row["training_load"] - 70) * 0.3
    return int(np.clip(round(score), 0, 100))


def risk_label(score):
    if score >= 70:
        return "정상"
    elif score >= 40:
        return "주의"
    return "위험"


def risk_color(label):
    return {"정상": GREEN, "주의": ORANGE, "위험": RED}[label]


def pick_label(score):
    if score >= 80:
        return "출전 권장"
    elif score >= 50:
        return "교체 활용"
    return "휴식 권고 (부상 위험)"


def generate_players(seed=42, n=30):
    rng = np.random.default_rng(seed)
    pos_list = ["GK"] * 3 + ["DF"] * 9 + ["MF"] * 9 + ["FW"] * 9
    rng.shuffle(pos_list)

    rows = []
    for i in range(n):
        pid = i + 1
        fatigue = int(rng.integers(1, 9))
        rpe = int(rng.integers(3, 10))
        pain_area, pain_level = "없음", 0
        if rng.random() < 0.22:
            pain_area = rng.choice(BODY_PARTS[1:])
            pain_level = int(rng.integers(2, 9))
        sleep_score = int(rng.integers(45, 96))
        training_load = int(rng.integers(40, 96))
        distance_km = round(float(rng.uniform(6, 11.5)), 1)
        sprint_count = int(rng.integers(8, 36))
        hr_avg = int(rng.integers(128, 176))

        rows.append(
            dict(
                id=pid,
                name=f"선수 {pid:02d}",
                position=pos_list[i],
                fatigue=fatigue,
                rpe=rpe,
                pain_area=pain_area,
                pain_level=pain_level,
                sleep_score=sleep_score,
                training_load=training_load,
                distance_km=distance_km,
                sprint_count=sprint_count,
                hr_avg=hr_avg,
            )
        )

    df = pd.DataFrame(rows)
    df["readiness_score"] = df.apply(compute_readiness, axis=1)
    df["risk_level"] = df["readiness_score"].apply(risk_label)
    return df


@st.cache_data
def generate_wearable_series(pid, days=14):
    rng = np.random.default_rng(1000 + pid)
    dates = [datetime.today() - timedelta(days=days - 1 - i) for i in range(days)]
    distance = np.clip(rng.normal(8.5, 1.3, days), 4, 13)
    hr = np.clip(rng.normal(150, 10, days), 110, 190)
    sleep = np.clip(rng.normal(75, 10, days), 40, 100)
    load = np.clip(rng.normal(70, 15, days), 20, 110)
    return pd.DataFrame(
        {
            "날짜": dates,
            "이동거리(km)": distance.round(1),
            "심박수(평균)": hr.round(0),
            "수면 점수": sleep.round(0),
            "훈련 부하": load.round(0),
        }
    )


@st.cache_data
def generate_season_trend(weeks=16):
    rng = np.random.default_rng(7)
    week_no = np.arange(1, weeks + 1)
    fitness = 60 + week_no * 1.8 + rng.normal(0, 2, weeks)
    management = 55 + week_no * 1.6 + rng.normal(0, 2, weeks)
    return pd.DataFrame(
        {
            "주차": week_no,
            "핵심 체력 점수": np.clip(fitness, 0, 100).round(1),
            "관리 능력 점수": np.clip(management, 0, 100).round(1),
        }
    )


# ----------------------------------------------------------------------
# 세션 상태 초기화
# ----------------------------------------------------------------------
if "players" not in st.session_state:
    st.session_state.players = generate_players()
if "seed" not in st.session_state:
    st.session_state.seed = 42


def update_player(pid, fatigue, rpe, pain_area, pain_level):
    df = st.session_state.players
    idx = df.index[df["id"] == pid][0]
    df.loc[idx, ["fatigue", "rpe", "pain_area", "pain_level"]] = [
        fatigue, rpe, pain_area, pain_level,
    ]
    new_score = compute_readiness(df.loc[idx])
    df.loc[idx, "readiness_score"] = new_score
    df.loc[idx, "risk_level"] = risk_label(new_score)
    st.session_state.players = df
    return new_score


# ----------------------------------------------------------------------
# 사이드바
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"## <span style='color:{PRIMARY}'>Play Ready</span>", unsafe_allow_html=True)
    st.caption("데이터로 확신을, 팀에게 승리를")
    st.divider()
    st.markdown("**TEAM 6 데모**")
    st.write("운동선수 감독을 위한 AI 기반 통합 컨디션 관리 플랫폼 데모입니다. 좌측 메뉴 대신 상단 탭에서 각 기능을 확인하세요.")
    st.divider()
    if st.button("🔄 선수단 데이터 새로 생성", use_container_width=True):
        st.session_state.seed += 1
        st.session_state.players = generate_players(seed=st.session_state.seed)
        st.cache_data.clear()
        st.rerun()

df = st.session_state.players

# ----------------------------------------------------------------------
# 헤더
# ----------------------------------------------------------------------
st.markdown(f"# <span style='color:{PRIMARY}'>Play Ready</span> ⚽", unsafe_allow_html=True)
st.caption("AI 기반 통합 컨디션 관리 플랫폼 — 자동 수집 / 선수 입력 / 감독 확인 기능 데모")

tab_team, tab_body, tab_guard, tab_pick, tab_grow = st.tabs(
    [
        "Team Ready (감독 대시보드)",
        "Body Ready (선수 입력)",
        "Guard Ready (웨어러블)",
        "Pick Ready (AI 출전 추천)",
        "Grow Ready (시즌 분석)",
    ]
)

# ----------------------------------------------------------------------
# TAB 1. Team Ready
# ----------------------------------------------------------------------
with tab_team:
    st.subheader("통합 대시보드 — 선수단 현황")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("전체 선수", f"{len(df)}명")
    c2.metric("🟢 정상", f"{(df.risk_level == '정상').sum()}명")
    c3.metric("🟠 주의", f"{(df.risk_level == '주의').sum()}명")
    c4.metric("🔴 위험", f"{(df.risk_level == '위험').sum()}명")

    st.markdown("#### 🚨 위험 선수 자동 알림")
    risky = df[df.risk_level == "위험"].sort_values("readiness_score")
    if risky.empty:
        st.success("현재 부상 임계치를 초과한 선수가 없습니다.")
    else:
        for _, r in risky.iterrows():
            pain_txt = f" · 통증 부위: {r.pain_area} (강도 {r.pain_level}/10)" if r.pain_area != "없음" else ""
            st.error(f"**{r['name']}** ({r.position}) · Readiness {r.readiness_score}점{pain_txt}")

    st.markdown("#### 선수단 Readiness Score")
    pos_filter = st.multiselect("포지션 필터", POSITIONS, default=POSITIONS)
    view = df[df.position.isin(pos_filter)].sort_values("readiness_score", ascending=False)
    view_display = view[["name", "position", "readiness_score", "risk_level", "fatigue", "pain_area", "sleep_score"]].rename(
        columns={
            "name": "선수",
            "position": "포지션",
            "readiness_score": "Readiness",
            "risk_level": "위험도",
            "fatigue": "피로도",
            "pain_area": "통증부위",
            "sleep_score": "수면점수",
        }
    )
    st.dataframe(
        view_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Readiness": st.column_config.ProgressColumn(
                "Readiness", min_value=0, max_value=100, format="%d점"
            ),
        },
    )

    fig = px.bar(
        view.sort_values("readiness_score"),
        x="readiness_score", y="name", orientation="h", color="risk_level",
        color_discrete_map={"정상": GREEN, "주의": ORANGE, "위험": RED},
        labels={"readiness_score": "Readiness Score", "name": "", "risk_level": "위험도"},
        height=max(400, 18 * len(view)),
    )
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# TAB 2. Body Ready
# ----------------------------------------------------------------------
with tab_body:
    st.subheader("Body Ready — 선수 직접 입력 (Today's Check-in)")
    st.caption("선수가 매일 아침 1분, 통증 부위와 피로도를 직접 기록합니다.")

    selected_name = st.selectbox("선수 선택", df["name"].tolist())
    row = df[df["name"] == selected_name].iloc[0]

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("##### 현재 컨디션 입력")
        fatigue = st.slider("피로도 (1~10)", 1, 10, int(row.fatigue))
        rpe = st.slider("RPE — 운동자각도 (1~10)", 1, 10, int(row.rpe))
        pain_area = st.selectbox("통증 부위 (3D 신체 모델 클릭 대체)", BODY_PARTS, index=BODY_PARTS.index(row.pain_area))
        pain_level = 0
        if pain_area != "없음":
            pain_level = st.slider("통증 강도 — VAS (1~10)", 1, 10, max(1, int(row.pain_level)))

        if st.button("✅ Check-in 제출", type="primary"):
            new_score = update_player(row.id, fatigue, rpe, pain_area, pain_level)
            st.success(f"제출 완료! {selected_name}님의 Readiness Score: **{new_score}점** ({risk_label(new_score)})")

    with col_b:
        st.markdown("##### 3D 신체 모형 — 통증 부위 표시")
        st.caption("마우스로 드래그하면 모형을 자유롭게 회전·확대할 수 있습니다.")
        body_fig = build_body_figure(pain_area, pain_level)
        st.plotly_chart(body_fig, use_container_width=True)
        if pain_area != "없음":
            st.warning(f"선택된 통증 부위: **{pain_area}** (강도 {pain_level}/10) — 모형에서 빨간색으로 표시됩니다.")
        else:
            st.info("현재 기록된 통증 부위가 없습니다.")

# ----------------------------------------------------------------------
# TAB 3. Guard Ready
# ----------------------------------------------------------------------
with tab_guard:
    st.subheader("Guard Ready — 웨어러블 자동 데이터 수집 (EPTS)")
    st.caption("GPS/IMU, 심박, 수면 센서를 통해 자동으로 수집되는 객관적 생체 데이터입니다.")

    sel = st.selectbox("선수 선택", df["name"].tolist(), key="guard_sel")
    pid = df[df["name"] == sel].iloc[0].id
    wdf = generate_wearable_series(pid)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("오늘 이동거리", f"{wdf['이동거리(km)'].iloc[-1]} km")
    m2.metric("평균 심박수", f"{int(wdf['심박수(평균)'].iloc[-1])} bpm")
    m3.metric("수면 점수", f"{int(wdf['수면 점수'].iloc[-1])}점")
    m4.metric("훈련 부하", f"{int(wdf['훈련 부하'].iloc[-1])}")

    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.line(wdf, x="날짜", y="이동거리(km)", markers=True, title="최근 14일 이동거리")
        fig1.update_traces(line_color=PRIMARY)
        st.plotly_chart(fig1, use_container_width=True)
        fig3 = px.line(wdf, x="날짜", y="수면 점수", markers=True, title="수면 질 추이")
        fig3.update_traces(line_color="#0EA5E9")
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        fig2 = px.line(wdf, x="날짜", y="심박수(평균)", markers=True, title="심박수 추이")
        fig2.update_traces(line_color=RED)
        st.plotly_chart(fig2, use_container_width=True)
        fig4 = px.bar(wdf, x="날짜", y="훈련 부하", title="훈련 부하(Training Load)")
        fig4.update_traces(marker_color=ORANGE)
        st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------------------------
# TAB 4. Pick Ready
# ----------------------------------------------------------------------
with tab_pick:
    st.subheader("Pick Ready — 데이터 기반 AI 출전 선수 추천")
    st.caption("포지션별 선수의 컨디션, 부상 위험, 경기 데이터를 종합 분석하여 최적의 선수를 추천합니다.")

    pos_choice = st.selectbox("포지션 선택", POSITIONS, index=POSITIONS.index("FW"))
    sub = df[df.position == pos_choice].sort_values("readiness_score", ascending=False)

    cols = st.columns(min(3, max(1, len(sub))))
    for i, (_, r) in enumerate(sub.head(3).iterrows()):
        label = pick_label(r.readiness_score)
        color = GREEN if label == "출전 권장" else ORANGE if label == "교체 활용" else RED
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div class="pr-card" style="background:{color}12;">
                  <div style="font-size:1rem;font-weight:600;">{r['name']}</div>
                  <div style="font-size:2rem;font-weight:800;color:{color};">{r.readiness_score}점</div>
                  <span class="pr-badge" style="background:{color};">{label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### 컨디션 현황판")
    full_sub = sub[["name", "readiness_score", "risk_level", "pain_area", "fatigue"]].rename(
        columns={"name": "선수", "readiness_score": "Readiness", "risk_level": "위험도", "pain_area": "통증부위", "fatigue": "피로도"}
    )
    st.dataframe(
        full_sub, use_container_width=True, hide_index=True,
        column_config={"Readiness": st.column_config.ProgressColumn("Readiness", min_value=0, max_value=100, format="%d점")},
    )

# ----------------------------------------------------------------------
# TAB 5. Grow Ready
# ----------------------------------------------------------------------
with tab_grow:
    st.subheader("Grow Ready — 시즌 성장 분석")
    st.caption("시즌 전체 데이터를 집계해 성장 추이와 부상 복구력, 진학 증빙 자료를 자동 생성합니다.")

    season = generate_season_trend()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=season["주차"], y=season["핵심 체력 점수"], mode="lines+markers", name="핵심 체력 점수", line=dict(color=PRIMARY)))
    fig.add_trace(go.Scatter(x=season["주차"], y=season["관리 능력 점수"], mode="lines+markers", name="관리 능력 점수", line=dict(color="#0EA5E9")))
    fig.update_layout(title="시즌 성장 추이", xaxis_title="주차", yaxis_title="점수", height=420)
    st.plotly_chart(fig, use_container_width=True)

    fit_growth = season["핵심 체력 점수"].iloc[-1] - season["핵심 체력 점수"].iloc[0]
    mgmt_growth = season["관리 능력 점수"].iloc[-1] - season["관리 능력 점수"].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("체력 성장률", f"+{fit_growth:.0f}%")
    c2.metric("관리 능력 성장률", f"+{mgmt_growth:.0f}%")
    c3.metric("출석률", "99%")

    st.markdown("#### 부상 복구력 데이터")
    injured = df[df.pain_area != "없음"][["name", "pain_area", "pain_level"]].copy()
    if injured.empty:
        st.info("현재 기록된 부상/통증 이력이 없습니다.")
    else:
        rng = np.random.default_rng(99)
        injured["부상 발생일"] = [
            (datetime.today() - timedelta(days=int(d))).strftime("%Y-%m-%d")
            for d in rng.integers(5, 60, len(injured))
        ]
        injured["예상 회복 기간(일)"] = (injured["pain_level"] * 3).clip(3, 30)
        injured = injured.rename(columns={"name": "선수", "pain_area": "부상 부위", "pain_level": "통증 강도"})
        st.dataframe(injured, use_container_width=True, hide_index=True)

    st.markdown("#### 진학 증빙 — 객관적 성실함 패키지")
    d1, d2, d3 = st.columns(3)
    d1.metric("출석률", "99%")
    d2.metric("데이터 완성도", "100%")
    d3.metric("훈련 일관성", "100%")
    st.download_button(
        "📄 증빙 패키지 내보내기 (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="play_ready_player_data.csv",
        mime="text/csv",
    )

st.divider()
st.caption("Play Ready Demo · TEAM 6 — 데이터로 확신을, 팀에게 승리를")
