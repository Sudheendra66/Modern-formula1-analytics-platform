"""
Formula 1 Analytics Platform - Main Dashboard
"""

from f1_ui.theme import load_theme
load_theme()

import streamlit as st
import pandas as pd
from snowflake_connection import get_connection
from f1_ui.theme import COLORS
from f1_ui.cards import hero_section, info_card, footer
from f1_ui.charts import styled_bar_chart, styled_scatter_chart


@st.cache_data(ttl=60)
def get_analytics_data():
    """Fetch all driver analytics from Snowflake."""
    conn = get_connection()
    return pd.read_sql("""
        select *
        from MART_DRIVER_ANALYTICS
        where DRIVER_NAME is not null
    """, conn)


@st.cache_data(ttl=60)
def get_goat_data():
    """Fetch GOAT-eligible ranked drivers from Snowflake."""
    conn = get_connection()
    return pd.read_sql("""
        select *
        from MART_DRIVER_RANKINGS
        where DRIVER_NAME is not null
        order by GOAT_RANK
    """, conn)


analytics = get_analytics_data()
goat_rankings = get_goat_data()


hero_section(
    title="Formula 1 Analytics Platform",
    subtitle="Performance analytics dashboard",
    icon=""
)


drivers = analytics["DRIVER_ID"].nunique()
races = analytics["TOTAL_RACES"].sum()
wins = analytics["WINS"].sum()
podiums = analytics["PODIUMS"].sum()
points = analytics["CAREER_POINTS"].sum()
best_goat = analytics["GOAT_SCORE"].max()


st.markdown("## 🏎️ Formula 1 Overview")

kpi_html = f"""
<style>
.kpi-grid {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
    margin-bottom:40px;
}}

.kpi-card {{
    background:#1B2333;
    border:1px solid #2D3748;
    border-radius:18px;
    padding:24px;
    transition:.3s;
    box-shadow:0 4px 15px rgba(0,0,0,.35);
}}

.kpi-card:hover {{
    transform:translateY(-6px);
    border-color:#E10600;
}}

.kpi-icon {{
    font-size:28px;
}}

.kpi-title {{
    color:#A0AEC0;
    font-size:16px;
    margin-top:10px;
}}

.kpi-value {{
    color:white;
    font-size:42px;
    font-weight:700;
    margin-top:12px;
}}
</style>

<div class="kpi-grid">

<div class="kpi-card">
<div class="kpi-icon">🏎️</div>
<div class="kpi-title">Total Drivers</div>
<div class="kpi-value">{drivers}</div>
</div>

<div class="kpi-card">
<div class="kpi-icon">🏁</div>
<div class="kpi-title">Grand Prix Events</div>
<div class="kpi-value">{races}</div>
</div>

<div class="kpi-card">
<div class="kpi-icon">🥇</div>
<div class="kpi-title">Total Wins</div>
<div class="kpi-value">{wins}</div>
</div>

<div class="kpi-card">
<div class="kpi-icon">🏆</div>
<div class="kpi-title">Total Podiums</div>
<div class="kpi-value">{podiums}</div>
</div>

<div class="kpi-card">
<div class="kpi-icon">⭐</div>
<div class="kpi-title">Career Points</div>
<div class="kpi-value">{points:,}</div>
</div>

<div class="kpi-card">
<div class="kpi-icon">👑</div>
<div class="kpi-title">Highest GOAT Score</div>
<div class="kpi-value">{best_goat:.2f}</div>
</div>

</div>
"""

st.markdown(kpi_html, unsafe_allow_html=True)

st.markdown("## 👑 GOAT Podium")

podium = goat_rankings.sort_values("GOAT_RANK").head(3)

cols = st.columns(3)

colors = [
    "#FFD700",
    "#C0C0C0",
    "#CD7F32"
]

medals = [
    "🥇",
    "🥈",
    "🥉"
]

for i, col in enumerate(cols):

    driver = podium.iloc[i]

    with col:

        st.markdown(
        f"""
<div style="
background:#1B2333;
padding:28px;
border-radius:22px;
border-top:6px solid {colors[i]};
box-shadow:0px 8px 25px rgba(0,0,0,.35);
text-align:center;
min-height:580px;
display:flex;
flex-direction:column;
justify-content:space-between;>

<div style="font-size:55px;">
{medals[i]}
</div>

<h2 style="color:white;margin-top:5px;">
#{driver["GOAT_RANK"]}<br>
{driver["DRIVER_NAME"]}
</h2>

<hr style="border:.5px solid #2D3748">

<h1 style="color:{colors[i]};">
{driver["GOAT_SCORE"]:.2f}
</h1>

<p style="color:#A0AEC0;font-size:18px;">
GOAT Score
</p>

<br>

<div style="
display:flex;
justify-content:space-around;
">

<div>
<h3 style="color:white;">{driver["WINS"]}</h3>
<p style="color:#A0AEC0;">Wins</p>
</div>

<div>
<h3 style="color:white;">{driver["PODIUMS"]}</h3>
<p style="color:#A0AEC0;">Podiums</p>
</div>

<div>
<h3 style="color:white;">{int(driver["CAREER_POINTS"]):,}</h3>
<p style="color:#A0AEC0;">Points</p>
</div>

</div>

</div>
""",
unsafe_allow_html=True
)
        
st.divider()

st.markdown("""
<h2 style="
color:white;
font-size:2rem;
margin-top:20px;
margin-bottom:20px;
">
📊 Performance Analysis
</h2>
""", unsafe_allow_html=True)

if len(goat_rankings) > 0:
    top10 = goat_rankings.sort_values("GOAT_RANK").head(10)
    fig_goat = styled_bar_chart(
        top10,
        x="DRIVER_NAME",
        y="GOAT_SCORE",
        title="Top 10 Drivers by GOAT Score",
        height=500
    )
    st.plotly_chart(fig_goat, use_container_width=True)

    fig_matrix = styled_scatter_chart(
        goat_rankings,
        x="WIN_RATE",
        y="PODIUM_RATE",
        size="CAREER_POINTS",
        color="GOAT_SCORE",
        hover_name="DRIVER_NAME",
        title="Driver Performance Matrix: Win Rate vs Podium Rate",
        height=600
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

st.divider()

st.markdown("### Complete GOAT Leaderboard")

control_col1, control_col2 = st.columns([2, 1])
with control_col1:
    search_term = st.text_input(
        "Search Driver",
        placeholder="Type driver name...",
        label_visibility="collapsed"
    )
with control_col2:
    top_n = st.selectbox(
        "Top N",
        options=[5, 10, 15, 20, 50],
        index=2,
        label_visibility="collapsed"
    )

filtered_rankings = goat_rankings.copy()
if search_term:
    filtered_rankings = filtered_rankings[
        filtered_rankings["DRIVER_NAME"].str.contains(search_term, case=False, na=False)
    ]

leaderboard_display = filtered_rankings.sort_values("GOAT_RANK").head(top_n)

if len(leaderboard_display) > 0:
    st.dataframe(
        leaderboard_display[[
            "GOAT_RANK",
            "DRIVER_NAME",
            "GOAT_SCORE",
            "CAREER_POINTS",
            "WINS",
            "PODIUMS",
            "WIN_RATE",
            "PODIUM_RATE",
            "TOTAL_RACES"
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "GOAT_RANK": st.column_config.NumberColumn("Rank", format="%d"),
            "DRIVER_NAME": "Driver",
            "GOAT_SCORE": st.column_config.NumberColumn("GOAT Score", format="%.2f"),
            "CAREER_POINTS": st.column_config.NumberColumn("Career Points", format="%.0f"),
            "WINS": st.column_config.NumberColumn("Wins", format="%d"),
            "PODIUMS": st.column_config.NumberColumn("Podiums", format="%d"),
            "WIN_RATE": st.column_config.NumberColumn("Win Rate %", format="%.2f"),
            "PODIUM_RATE": st.column_config.NumberColumn("Podium Rate %", format="%.2f"),
            "TOTAL_RACES": st.column_config.NumberColumn("Races", format="%d"),
        }
    )

    csv = leaderboard_display.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="f1_analytics_leaderboard.csv",
        mime="text/csv"
    )

st.divider()

st.markdown("### GOAT Score Methodology")
info_card(
    title="How GOAT Score is calculated",
    items=[
        ("Career Points", "35%"),
        ("Wins", "25%"),
        ("Podiums", "20%"),
        ("Win Rate", "10%"),
        ("Podium Rate", "10%"),
        ("Eligibility", "50+ races and 300+ career points"),
    ],
    icon=""
)

footer()