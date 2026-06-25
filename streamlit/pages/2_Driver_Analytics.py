"""
Driver Analytics Page - Individual Driver Performance Analysis
"""

from f1_ui.theme import load_theme
load_theme()

import streamlit as st
import pandas as pd
from snowflake_connection import get_connection
from f1_ui.cards import hero_section, info_card, footer, progress_bar
from f1_ui.charts import styled_bar_chart
from f1_ui.theme import COLORS

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="📊 Driver Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# DATA CONNECTION
# =====================================================

@st.cache_data(ttl=60)
def get_driver_analytics():
    """Fetch driver analytics from Snowflake (cached)."""
    conn = get_connection()
    return pd.read_sql("""
        select *
        from MART_DRIVER_ANALYTICS
    """, conn)


df = get_driver_analytics()
ranked_df = df.dropna(subset=["GOAT_SCORE", "GOAT_RANK"]).copy()


def fmt_goat_score(value):
    return "Not eligible" if pd.isna(value) else f"{value:.2f}"


def fmt_goat_rank(value):
    return "Not eligible" if pd.isna(value) else f"#{int(value)}"

# =====================================================
# HERO SECTION
# =====================================================

hero_section(
    title="Driver Analytics",
    subtitle="Deep-dive performance analysis for individual drivers",
    icon="📊"
)

# =====================================================
# DRIVER SELECTION
# =====================================================

st.markdown("### 🏎️ Select Driver")

driver = st.selectbox(
    "Choose a driver to analyze",
    sorted(df["DRIVER_NAME"].dropna().unique()),
    label_visibility="collapsed"
)

selected = df[df["DRIVER_NAME"] == driver].iloc[0]

st.divider()

# =====================================================
# DRIVER PROFILE
# =====================================================

st.markdown(f"### 👤 {selected['DRIVER_NAME']} Profile")

profile_col1, profile_col2 = st.columns([1, 2])

with profile_col1:
    # Basic metrics
    st.markdown("**Basic Stats**")
    st.metric("Races Competed", int(selected["TOTAL_RACES"]))
    st.metric("Career Points", f"{selected['CAREER_POINTS']:,.0f}")
    st.metric("GOAT Rank", fmt_goat_rank(selected["GOAT_RANK"]))

with profile_col2:
    # Create info card for detailed metrics
    info_card(
        title="Performance Summary",
        items=[
            ("GOAT Score", fmt_goat_score(selected["GOAT_SCORE"])),
            ("Wins", f"{int(selected['WINS'])}"),
            ("Podiums", f"{int(selected['PODIUMS'])}"),
            ("Poles", f"{int(selected.get('POLE_POSITIONS', 0))}"),
            ("Win Rate", f"{selected['WIN_RATE']:.2f}%"),
            ("Podium Rate", f"{selected['PODIUM_RATE']:.2f}%"),
        ],
        icon="📊"
    )

st.divider()

# =====================================================
# PERFORMANCE METRICS
# =====================================================

st.markdown("### 📈 Performance Metrics")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("🏆 Podiums", int(selected["PODIUMS"]))
with metric_col2:
    st.metric("🥇 Wins", int(selected["WINS"]))
with metric_col3:
    st.metric("⭐ Win Rate", f"{selected['WIN_RATE']:.2f}%")
with metric_col4:
    st.metric("🎯 Podium Rate", f"{selected['PODIUM_RATE']:.2f}%")

st.divider()

# =====================================================
# PROGRESS BARS
# =====================================================

st.markdown("### 📊 Score Breakdown")

# Calculate percentage scores relative to dataset max
max_points = df["CAREER_POINTS"].max()
max_wins = df["WINS"].max()
max_podiums = df["PODIUMS"].max()
max_goat = ranked_df["GOAT_SCORE"].max() if len(ranked_df) > 0 else 0

progress_bar(
    "Career Points",
    selected["CAREER_POINTS"],
    max_points,
    COLORS["gold"]
)

progress_bar(
    "Wins",
    selected["WINS"],
    max_wins,
    COLORS["accent"]
)

progress_bar(
    "Podiums",
    selected["PODIUMS"],
    max_podiums,
    COLORS["silver"]
)

progress_bar(
    "GOAT Score",
    (0 if pd.isna(selected["GOAT_SCORE"]) else selected["GOAT_SCORE"]),
    max_goat,
    COLORS["accent"]
)

st.divider()

# =====================================================
# COMPARISON WITH TOP DRIVERS
# =====================================================

st.markdown("### 🏁 Comparison with Top 5")

top_5 = ranked_df.nlargest(5, "GOAT_SCORE").copy()
comparison_df = pd.concat([pd.DataFrame([selected]), top_5[~(top_5["DRIVER_NAME"] == driver)].head(4)])

fig = styled_bar_chart(
    comparison_df,
    x="DRIVER_NAME",
    y="GOAT_SCORE",
    title=f"{selected['DRIVER_NAME']} vs Top Drivers",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# FULL DATASET
# =====================================================

st.markdown("### 📋 All Drivers Comparison")

comparison_table = ranked_df[[
    "GOAT_RANK",
    "DRIVER_NAME",
    "GOAT_SCORE",
    "CAREER_POINTS",
    "WINS",
    "PODIUMS"
]].head(20).copy()

st.dataframe(
    comparison_table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "GOAT_RANK": st.column_config.NumberColumn("Rank", format="%d"),
        "DRIVER_NAME": "Driver",
        "GOAT_SCORE": st.column_config.NumberColumn("GOAT Score", format="%.2f"),
        "CAREER_POINTS": st.column_config.NumberColumn("Career Points", format="%.0f"),
        "WINS": st.column_config.NumberColumn("Wins", format="%d"),
        "PODIUMS": st.column_config.NumberColumn("Podiums", format="%d"),
    }
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

footer()