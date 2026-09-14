import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 기본 설정
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

df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

# 컬럼명 정리
df.columns = df.columns.str.strip()

# 영화명 정리
df["영화명"] = df["영화명"].astype(str).str.strip()

# 날짜 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str).str.strip(),
    format="%Y%m%d",
    errors="coerce"
)

# 일관객 숫자 변환
df["일관객"] = pd.to_numeric(
    df["일관객"],
    errors="coerce"
)

# 필요한 데이터가 없는 행 제거
df = df.dropna(
    subset=["날짜", "영화명", "일관객"]
)


# ============================================================
# 그래프 1
# ============================================================

st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

movie_list = sorted(df["영화명"].unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[
    df["영화명"] == selected_movie
].copy()

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

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 2
# ============================================================

st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 TOP 5")

movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

top5_movies = movie_total.head(5).index.tolist()

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

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

daily_total = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)

top3_days = daily_total.nlargest(
    3,
    "일관객"
)

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

# 관객이 가장 많았던 3일 표시
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

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 4
# ============================================================

st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        일수=("날짜", "nunique")
    )
    .reset_index()
)

top10 = (
    movie_summary
    .sort_values(
        "일관객합계",
        ascending=False
    )
    .head(10)
    .copy()
)

# 가로 막대그래프에서 높은 값이 위에 오도록
top10 = top10.sort_values(
    "일관객합계",
    ascending=True
)

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

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")


# ============================================================
# 그래프 5
# ============================================================

st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "월과 요일에 따른 일관객 합계를 히트맵으로 나타냅니다."
)


# ------------------------------------------------------------
# 날짜에서 월과 요일 추출
# ------------------------------------------------------------

df["월"] = df["날짜"].dt.month

weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

df["요일"] = df["날짜"].dt.dayofweek.map(
    weekday_map
)


# ------------------------------------------------------------
# 요일 순서
# ------------------------------------------------------------

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


# ------------------------------------------------------------
# 월 × 요일별 일관객 합계 계산
# ------------------------------------------------------------

heatmap_data = (
    df.groupby(
        ["월", "요일"]
    )["일관객"]
    .sum()
    .unstack(
        fill_value=0
    )
)

# 월요일 → 일요일 순서로 정렬
heatmap_data = heatmap_data.reindex(
    columns=weekday_order,
    fill_value=0
)

# 월 순서 정렬
heatmap_data = heatmap_data.sort_index()


# ------------------------------------------------------------
# 히트맵
# ------------------------------------------------------------

fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=weekday_order,
        y=[
            f"{month}월"
            for month in heatmap_data.index
        ],
        colorscale="Blues",
        colorbar=dict(
            title="일관객 합계"
        ),
        hovertemplate=
        "월: %{y}"
        "<br>요일: %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    title="월 × 요일별 일관객 합계",
    xaxis_title="요일",
    yaxis_title="월"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.write("")
