import streamlit as st
import pandas as pd
import plotly.express as px

from snowflake_connection import get_connection

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="🏎️ Formula 1 Analytics Platform (2020-2026)",
    page_icon="🏎️",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------
st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #111827;
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1F2937;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Headers */
h1,h2,h3,h4 {
    color: white !important;
}

/* Text */
p,label,span {
    color: #E5E7EB !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #1F2937;
    border-left: 5px solid #E10600;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

[data-testid="metric-container"] * {
    color: white !important;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    background-color: #1F2937 !important;
    border-radius: 10px;
    padding: 5px;
}

/* Tables */
table {
    color: white !important;
}

thead tr th {
    background-color: #E10600 !important;
    color: white !important;
}

tbody tr {
    background-color: #1F2937 !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    color: white !important;
}

/* Divider */
hr {
    border-color: #374151 !important;
}

</style>
""", unsafe_allow_html=True)
# ------------------------------------------------
# CONNECTION
# ------------------------------------------------

conn = get_connection()

analytics = pd.read_sql("""
select *
from MART_DRIVER_ANALYTICS
where DRIVER_NAME is not null
""", conn)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("🏎️ Formula 1 Analytics Platform (2020-2026)")

st.markdown("""
### Modern Formula 1 Performance Analytics

Analyze driver performance, rankings, win rates, podium rates and GOAT scores across the modern Formula 1 era (2020-2026).
""")

# ------------------------------------------------
# GOAT EXPLANATION
# ------------------------------------------------

with st.expander("ℹ️ How is GOAT Score Calculated?"):

    st.markdown("""
**GOAT Score** is a custom performance metric designed to rank Formula 1 drivers.

Formula:

**GOAT Score =**

- 40% Win Rate
- 30% Podium Rate
- 30% Points Per Race

This balances:

- Winning ability
- Consistency
- Points accumulation

Higher scores indicate stronger overall driver performance.
""")

# ------------------------------------------------
# TOP 3 DRIVERS
# ------------------------------------------------

top3 = analytics.sort_values(
    "GOAT_SCORE",
    ascending=False
).head(3)

st.subheader("👑 Current GOAT Podium")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🥇 GOAT #1",
        top3.iloc[0]["DRIVER_NAME"],
        f"Score {round(top3.iloc[0]['GOAT_SCORE'],2)}"
    )

with c2:
    st.metric(
        "🥈 GOAT #2",
        top3.iloc[1]["DRIVER_NAME"],
        f"Score {round(top3.iloc[1]['GOAT_SCORE'],2)}"
    )

with c3:
    st.metric(
        "🥉 GOAT #3",
        top3.iloc[2]["DRIVER_NAME"],
        f"Score {round(top3.iloc[2]['GOAT_SCORE'],2)}"
    )

st.divider()

# ------------------------------------------------
# KPI SECTION
# ------------------------------------------------

drivers = analytics["DRIVER_ID"].nunique()
races = analytics["TOTAL_RACES"].sum()
wins = analytics["WINS"].sum()
podiums = analytics["PODIUMS"].sum()
points = analytics["CAREER_POINTS"].sum()
best_goat = analytics["GOAT_SCORE"].max()

col1, col2, col3 = st.columns(3)

col1.metric("🏎️ Drivers", int(drivers))
col2.metric("🏁 Total Races", int(races))
col3.metric("🥇 Wins", int(wins))

col1, col2, col3 = st.columns(3)

col1.metric("🏆 Podiums", int(podiums))
col2.metric("⭐ Career Points", f"{int(points):,}")
col3.metric("👑 Best GOAT Score", round(best_goat, 2))

st.divider()

# ------------------------------------------------
# TOP 10 GOAT DRIVERS
# ------------------------------------------------
leaderboard = analytics.sort_values(
    "GOAT_RANK"
)

st.subheader("🏆 GOAT Leaderboard")

top10 = analytics.sort_values(
    "GOAT_SCORE",
    ascending=False
).head(10)

fig = px.bar(
    top10,
    x="DRIVER_NAME",
    y="GOAT_SCORE",
    color="GOAT_SCORE",
    text="GOAT_SCORE",
    title="Top 10 Drivers by GOAT Score",
    color_continuous_scale="Reds"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# PERFORMANCE MATRIX
# ------------------------------------------------

st.subheader("📊 Driver Performance Matrix")

fig2 = px.scatter(
    analytics,
    x="WIN_RATE",
    y="PODIUM_RATE",
    size="CAREER_POINTS",
    color="GOAT_SCORE",
    hover_name="DRIVER_NAME",
    color_continuous_scale="Turbo"
)

fig2.update_layout(
    template="plotly_dark",
    height=700,
    paper_bgcolor="#0B0F19",
    plot_bgcolor="#0B0F19"
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------
# LEADERBOARD
# ------------------------------------------------

st.subheader("🏁 GOAT Leaderboard")

leaderboard = analytics.sort_values(
    "GOAT_RANK"
)

st.dataframe(
    leaderboard[
        [
            "GOAT_RANK",
            "DRIVER_NAME",
            "GOAT_SCORE",
            "CAREER_POINTS",
            "WINS",
            "PODIUMS",
            "WIN_RATE",
            "PODIUM_RATE"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Formula 1 Analytics Platform (2020-2026) • Snowflake • dbt • Streamlit • Custom Fivetran Connector"
)