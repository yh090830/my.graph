import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 실제 날짜로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

# 일관객을 숫자로 변환
df["일관객"] = pd.to_numeric(
    df["일관객"],
    errors="coerce"
)

# 영화명이 없는 행 제거
df = df.dropna(subset=["영화명", "날짜", "일관객"])


# ============================================================
# 그래프 1
# ============================================================

st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

movie_list = sorted(df["영화명"].unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}"
    "<br>일관객: %{y:,}명"
    "<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 2
# ============================================================

st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 TOP 5")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편의 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 일관객 합계
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# TOP 5 영화명
top5_movies = movie_total.head(5).index.tolist()

# TOP 5 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}"
    "<br>날짜: %{x|%Y-%m-%d}"
    "<br>일관객: %{y:,}명"
    "<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 10위권 영화들의 일관객을 모두 더해 "
    "날짜별 전체 관객 규모를 보여 줍니다."
)

# 날짜별 일관객 합계
daily_total = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일
top3_days = (
    daily_total
    .nlargest(3, "일관객")
)

# 영역 그래프
fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=daily_total["날짜"],
        y=daily_total["일관객"],
        mode="lines",
        fill="tozeroy",
        name="10위권 일관객 합계",
        hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 가장 컸던 3일 표시
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10
    )

fig3.update_layout(
    title="날짜별 10위권 일관객 합계",
    xaxis_title="날짜",
    yaxis_title="일관객 합계(명)"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 4
# ============================================================

st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "이 기간 동안 영화별 일관객을 모두 더해 "
    "관객이 가장 많았던 영화 10편을 보여 줍니다."
)


# ------------------------------------------------------------
# 영화별 일관객 합계
# ------------------------------------------------------------

movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        일수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계 TOP 10
top10 = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)

# 그래프에서는 관객이 많은 영화가 위에 오도록
top10 = top10.sort_values("일관객합계", ascending=True)


# ------------------------------------------------------------
# 가로 막대그래프
# ------------------------------------------------------------

fig4 = px.bar(
    top10,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "기간 일관객 합계"
    },
    custom_data=["일수"]
)

fig4.update_traces(
    hovertemplate=
    "영화: %{y}"
    "<br>기간 일관객 합계: %{x:,}명"
    "<br>10위권에 든 날수: %{customdata[0]}일"
    "<extra></extra>"
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계(명)",
    yaxis_title="영화"
)

st.plotly_chart(fig4, use_container_width=True)


# ------------------------------------------------------------
# 그래프 4 설명 자리
# ------------------------------------------------------------

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 다음 그래프를 위한 공간
# ============================================================

st.divider()

st.header("그래프 5")
st.write("앞으로 추가할 그래프를 위한 공간입니다.")
