"""
Driver Comparison Page - Compare Two Drivers Head-to-Head
"""

from f1_ui.theme import load_theme
load_theme()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from snowflake_connection import get_connection
from f1_ui.cards import hero_section, info_card, footer
from f1_ui.charts import styled_bar_chart
from f1_ui.theme import COLORS

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="⚔️ Driver Comparison",
    page_icon="⚔️",
    layout="wide"
)

# =====================================================
# DATA CONNECTION
# =====================================================

@st.cache_data(ttl=60)
def get_comparison_data():
    """Fetch comparison data from Snowflake (cached)."""
    conn = get_connection()
    return pd.read_sql("""
        select *
        from MART_DRIVER_ANALYTICS
    """, conn)


df = get_comparison_data()
ranked_df = df.dropna(subset=["GOAT_SCORE", "GOAT_RANK"]).copy()


def fmt_goat_score(value):
    return "Not eligible" if pd.isna(value) else f"{value:.2f}"


def fmt_goat_rank(value):
    return "Not eligible" if pd.isna(value) else f"#{int(value)}"


def goat_delta(left, right):
    if pd.isna(left) or pd.isna(right):
        return None
    return f"{left - right:.2f}"

# =====================================================
# HERO SECTION
# =====================================================

hero_section(
    title="Driver Comparison",
    subtitle="Head-to-head comparison of driver performance metrics",
    icon="⚔️"
)

# =====================================================
# DRIVER SELECTION
# =====================================================

st.markdown("### 🏎️ Select Drivers to Compare")

comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    driver1 = st.selectbox(
        "First Driver",
        sorted(df["DRIVER_NAME"].dropna().unique()),
        index=0,
        label_visibility="collapsed"
    )

with comp_col2:
    driver2 = st.selectbox(
        "Second Driver",
        sorted(df["DRIVER_NAME"].dropna().unique()),
        index=1,
        label_visibility="collapsed"
    )

if driver1 == driver2:
    st.warning("Please select two different drivers for comparison.")
else:
    
    # Get selected drivers data
    driver1_data = df[df["DRIVER_NAME"] == driver1].iloc[0]
    driver2_data = df[df["DRIVER_NAME"] == driver2].iloc[0]

    st.divider()

    # =====================================================
    # SIDE-BY-SIDE PROFILE
    # =====================================================

    st.markdown("### 👥 Profile Comparison")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        info_card(
            title=driver1_data["DRIVER_NAME"],
            items=[
                ("GOAT Score", fmt_goat_score(driver1_data["GOAT_SCORE"])),
                ("Rank", fmt_goat_rank(driver1_data["GOAT_RANK"])),
                ("Career Points", f"{driver1_data['CAREER_POINTS']:,.0f}"),
                ("Wins", f"{int(driver1_data['WINS'])}"),
                ("Podiums", f"{int(driver1_data['PODIUMS'])}"),
                ("Races", f"{int(driver1_data['TOTAL_RACES'])}"),
            ],
            icon="🏎️"
        )

    with profile_col2:
        info_card(
            title=driver2_data["DRIVER_NAME"],
            items=[
                ("GOAT Score", fmt_goat_score(driver2_data["GOAT_SCORE"])),
                ("Rank", fmt_goat_rank(driver2_data["GOAT_RANK"])),
                ("Career Points", f"{driver2_data['CAREER_POINTS']:,.0f}"),
                ("Wins", f"{int(driver2_data['WINS'])}"),
                ("Podiums", f"{int(driver2_data['PODIUMS'])}"),
                ("Races", f"{int(driver2_data['TOTAL_RACES'])}"),
            ],
            icon="🏎️"
        )

    st.divider()

    # =====================================================
    # METRICS COMPARISON
    # =====================================================

    st.markdown("### 📊 Key Metrics Comparison")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            "Career Points",
            f"{driver1_data['CAREER_POINTS']:,.0f}",
            f"{int(driver1_data['CAREER_POINTS'] - driver2_data['CAREER_POINTS'])}"
        )
        st.metric(
            "",
            f"{driver2_data['CAREER_POINTS']:,.0f}",
            label_visibility="collapsed"
        )

    with metric_col2:
        st.metric(
            "Wins",
            int(driver1_data['WINS']),
            int(driver1_data['WINS'] - driver2_data['WINS'])
        )
        st.metric(
            "",
            int(driver2_data['WINS']),
            label_visibility="collapsed"
        )

    with metric_col3:
        st.metric(
            "Podiums",
            int(driver1_data['PODIUMS']),
            int(driver1_data['PODIUMS'] - driver2_data['PODIUMS'])
        )
        st.metric(
            "",
            int(driver2_data['PODIUMS']),
            label_visibility="collapsed"
        )

    with metric_col4:
        st.metric(
            "GOAT Score",
            fmt_goat_score(driver1_data["GOAT_SCORE"]),
            goat_delta(driver1_data["GOAT_SCORE"], driver2_data["GOAT_SCORE"])
        )
        st.metric(
            "",
            fmt_goat_score(driver2_data["GOAT_SCORE"]),
            label_visibility="collapsed"
        )

    st.divider()

    # =====================================================
    # RADAR CHART
    # =====================================================

    st.markdown("### 📈 Performance Radar Chart")

    # Normalize metrics to 0-100 scale for radar chart
    max_points = df["CAREER_POINTS"].max()
    max_wins = df["WINS"].max()
    max_podiums = df["PODIUMS"].max()
    max_goat = ranked_df["GOAT_SCORE"].max() if len(ranked_df) > 0 else 0
    max_rate = 100

    driver1_radar = [
        (driver1_data["CAREER_POINTS"] / max_points) * 100,
        (driver1_data["WINS"] / max_wins) * 100,
        (driver1_data["PODIUMS"] / max_podiums) * 100,
        driver1_data["WIN_RATE"],
        driver1_data["PODIUM_RATE"],
    ]

    driver2_radar = [
        (driver2_data["CAREER_POINTS"] / max_points) * 100,
        (driver2_data["WINS"] / max_wins) * 100,
        (driver2_data["PODIUMS"] / max_podiums) * 100,
        driver2_data["WIN_RATE"],
        driver2_data["PODIUM_RATE"],
    ]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=driver1_radar,
        theta=["Career Points", "Wins", "Podiums", "Win Rate %", "Podium Rate %"],
        fill='toself',
        name=driver1_data["DRIVER_NAME"],
        line=dict(color=COLORS["accent"]),
        fillcolor="rgba(225, 6, 0, 0.3)"
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=driver2_radar,
        theta=["Career Points", "Wins", "Podiums", "Win Rate %", "Podium Rate %"],
        fill='toself',
        name=driver2_data["DRIVER_NAME"],
        line=dict(color=COLORS["gold"]),
        fillcolor="rgba(255, 215, 0, 0.2)"
    ))

    fig_radar.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["text_primary"]),
        height=600,
        showlegend=True,
        legend=dict(x=1.1, y=1, bgcolor="rgba(0,0,0,0)"),
        polar=dict(
            bgcolor=COLORS["card_bg"],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=COLORS["text_secondary"]),
                gridcolor=COLORS["border"]
            ),
            angularaxis=dict(
                tickfont=dict(color=COLORS["text_secondary"])
            )
        )
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()

    # =====================================================
    # BAR CHART COMPARISON
    # =====================================================

    st.markdown("### 📊 Detailed Metrics Bar Chart")

    comparison_metrics = pd.DataFrame({
        "Metric": ["Career Points", "Wins", "Podiums", "Races"],
        driver1_data["DRIVER_NAME"]: [
            driver1_data["CAREER_POINTS"],
            driver1_data["WINS"],
            driver1_data["PODIUMS"],
            driver1_data["TOTAL_RACES"]
        ],
        driver2_data["DRIVER_NAME"]: [
            driver2_data["CAREER_POINTS"],
            driver2_data["WINS"],
            driver2_data["PODIUMS"],
            driver2_data["TOTAL_RACES"]
        ]
    })

    # Melt for grouped bar chart
    comparison_melted = comparison_metrics.melt(
        id_vars=["Metric"],
        var_name="Driver",
        value_name="Value"
    )

    # Create bar chart for comparison
    import plotly.express as px
    fig_comparison = px.bar(
        comparison_melted,
        x="Metric",
        y="Value",
        color="Driver",
        barmode="group",
        template="plotly_dark",
        title="Detailed Performance Comparison"
    )

    fig_comparison.update_layout(
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["text_primary"]),
        height=500,
        xaxis=dict(
            tickfont=dict(color=COLORS["text_primary"]),
            gridcolor=COLORS["border"]
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS["text_primary"]),
            gridcolor=COLORS["border"]
        )
    )

    fig_comparison.update_traces(
        marker=dict(
            line=dict(color=COLORS["card_bg"], width=1),
            opacity=0.9
        )
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

    st.divider()

    # =====================================================
    # FOOTER
    # =====================================================

    footer()
