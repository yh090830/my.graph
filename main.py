import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("영화의 날짜별 일관객 변화를 살펴보는 그래프입니다.")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 실제 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)

# 숫자형 열 변환
numeric_columns = [
    "순위",
    "영화코드",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# 그래프 1
# ============================================================

st.header("그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write("영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다.")

# 영화 선택
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화의 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")

# 선 그래프
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

# 마우스를 올렸을 때 날짜와 관객수가 보이도록 설정
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(fig1, use_container_width=True)


# ------------------------------------------------------------
# 그래프 1 설명 자리
# ------------------------------------------------------------

st.markdown("### 이 그래프로 알 수 있는 것")

st.write("")


# ============================================================
# 그래프 2
# ============================================================

st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 TOP 5")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)


# ------------------------------------------------------------
# 기간 전체에서 영화별 일관객 합계 계산
# ------------------------------------------------------------

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

# 일관객 합계가 가장 큰 5편
top5_movies = movie_totals.head(5)["영화명"].tolist()


# ------------------------------------------------------------
# TOP 5 영화만 골라내기
# ------------------------------------------------------------

top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜순으로 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])


# ------------------------------------------------------------
# TOP 5 날짜별 일관객 선 그래프
# ------------------------------------------------------------

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

# 마우스를 올렸을 때 날짜, 영화명, 관객수가 보이도록 설정
fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화"
)

# 그래프 표시
st.plotly_chart(
    fig2,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 2 설명 자리
# ------------------------------------------------------------

st.markdown("### 이 그래프로 알 수 있는 것")

st.write("")


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("그래프 3")
st.write("앞으로 추가할 그래프를 위한 공간입니다.")


# ============================================================
# 그래프 4
# ============================================================

st.divider()

st.header("그래프 4")
st.write("앞으로 추가할 그래프를 위한 공간입니다.")
