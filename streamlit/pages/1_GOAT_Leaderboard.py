"""
GOAT Leaderboard Page - Premium Ranking Dashboard
"""

from f1_ui.theme import load_theme
load_theme()

import streamlit as st
import pandas as pd
from snowflake_connection import get_connection
from f1_ui.cards import hero_section, progress_bar, footer
from f1_ui.theme import COLORS

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="👑 GOAT Leaderboard",
    page_icon="👑",
    layout="wide"
)

# =====================================================
# DATA CONNECTION
# =====================================================

@st.cache_data(ttl=60)
def get_leaderboard_data():
    """Fetch leaderboard data from Snowflake (cached)."""
    conn = get_connection()
    return pd.read_sql("""
        select *
        from MART_DRIVER_RANKINGS
        where DRIVER_NAME is not null
        order by GOAT_RANK
    """, conn)


df = get_leaderboard_data()

# =====================================================
# HERO SECTION
# =====================================================

hero_section(
    title="GOAT Leaderboard",
    subtitle="Complete ranking of Formula 1 drivers by GOAT Score",
    icon="👑"
)

# =====================================================
# CONTROLS & FILTERS
# =====================================================

st.markdown("### 🔍 Filter & Search")

control_col1, control_col2, control_col3 = st.columns([2, 1, 1])

with control_col1:
    search_term = st.text_input(
        "Search Driver",
        placeholder="Type driver name...",
        label_visibility="collapsed"
    )

with control_col2:
    min_races = st.number_input(
        "Min Races",
        value=50,
        min_value=50,
        label_visibility="collapsed"
    )

with control_col3:
    top_n = st.selectbox(
        "Top N",
        options=[10, 20, 50, 100],
        index=1,
        label_visibility="collapsed"
    )

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df.copy()

# Apply search filter
if search_term:
    filtered_df = filtered_df[
        filtered_df["DRIVER_NAME"].str.contains(search_term, case=False, na=False)
    ]

# Apply races filter
filtered_df = filtered_df[filtered_df["TOTAL_RACES"] >= min_races]

# Limit to top N
filtered_df = filtered_df.head(top_n)

# =====================================================
# STATS ROW
# =====================================================

st.markdown(f"**Results:** {len(filtered_df)} drivers")

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.metric("🏆 Top GOAT Score", f"{filtered_df['GOAT_SCORE'].max():.2f}")
with stat_col2:
    st.metric("👤 Average GOAT Score", f"{filtered_df['GOAT_SCORE'].mean():.2f}")
with stat_col3:
    st.metric("🏁 Average Races", f"{filtered_df['TOTAL_RACES'].mean():.0f}")

st.divider()

# =====================================================
# LEADERBOARD TABLE
# =====================================================

st.markdown("### 🏁 Rankings")

# Display with formatted columns
display_df = filtered_df[[
    "GOAT_RANK",
    "DRIVER_NAME",
    "GOAT_SCORE",
    "CAREER_POINTS",
    "WINS",
    "PODIUMS",
    "WIN_RATE",
    "PODIUM_RATE",
    "TOTAL_RACES"
]].copy()

# Rename for display
display_df.columns = [
    "Rank",
    "Driver",
    "GOAT Score",
    "Career Points",
    "Wins",
    "Podiums",
    "Win Rate %",
    "Podium Rate %",
    "Races"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", format="%d"),
        "Driver": "Driver Name",
        "GOAT Score": st.column_config.NumberColumn("GOAT Score", format="%.2f"),
        "Career Points": st.column_config.NumberColumn("Career Points", format="%.0f"),
        "Wins": st.column_config.NumberColumn("Wins", format="%d"),
        "Podiums": st.column_config.NumberColumn("Podiums", format="%d"),
        "Win Rate %": st.column_config.NumberColumn("Win Rate %", format="%.2f"),
        "Podium Rate %": st.column_config.NumberColumn("Podium Rate %", format="%.2f"),
        "Races": st.column_config.NumberColumn("Races", format="%d"),
    }
)

st.divider()

# =====================================================
# PROGRESS BARS
# =====================================================

st.markdown("### 📊 Top 10 Progress")

top_10_progress = filtered_df.head(10).copy()

for idx, row in top_10_progress.iterrows():
    progress_bar(
        label=f"{int(row['GOAT_RANK'])}. {row['DRIVER_NAME']}",
        value=row['GOAT_SCORE'],
        max_value=df['GOAT_SCORE'].max(),
        color=COLORS["accent"]
    )

st.divider()

# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.markdown("### 📥 Export")

csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=csv,
    file_name="f1_goat_leaderboard.csv",
    mime="text/csv",
    key="download_csv"
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

footer()

