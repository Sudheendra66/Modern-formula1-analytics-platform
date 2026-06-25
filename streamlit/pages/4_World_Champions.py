"""
World Champions Page - Season-by-Season Champion History
"""

from f1_ui.theme import load_theme
load_theme()

import streamlit as st
import pandas as pd
from snowflake_connection import get_connection
from f1_ui.cards import hero_section, info_card, footer
from f1_ui.theme import COLORS

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="🏆 World Champions",
    page_icon="🏆",
    layout="wide"
)

# =====================================================
# DATA CONNECTION
# =====================================================

@st.cache_data(ttl=60)
def get_champions_data():
    """Fetch champions data from Snowflake (cached)."""
    conn = get_connection()
    
    # Get standings data to identify champions by season
    standings = pd.read_sql("""
        select *
        from STG_DRIVER_STANDINGS
        where POSITION = 1
        order by SEASON DESC, POSITION
    """, conn)
    
    return standings


try:
    champions_df = get_champions_data()
    has_champions_data = len(champions_df) > 0
except:
    has_champions_data = False
    champions_df = pd.DataFrame()

# =====================================================
# HERO SECTION
# =====================================================

hero_section(
    title="World Champions",
    subtitle="Season-by-season championship history",
    icon="🏆"
)

# =====================================================
# CHAMPIONS DISPLAY
# =====================================================

if has_champions_data and len(champions_df) > 0:
    
    # Get correct driver name column
    driver_col = None
    for col in champions_df.columns:
        if 'driver' in col.lower() and 'name' in col.lower():
            driver_col = col
            break
    if not driver_col:
        driver_col = champions_df.columns[1] if len(champions_df.columns) > 1 else None
    
    # Get unique seasons and count
    seasons = sorted(champions_df["SEASON"].unique(), reverse=True)
    
    st.markdown(f"### 🏅 Champions ({len(seasons)} Seasons)")
    
    # Summary stats
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("🏆 Total Seasons", len(seasons))
    
    with summary_col2:
        if driver_col and driver_col in champions_df.columns:
            unique_champs = champions_df[driver_col].nunique()
            st.metric("👤 Unique Champions", unique_champs)
        else:
            st.metric("👤 Unique Champions", "N/A")
    
    with summary_col3:
        if driver_col and driver_col in champions_df.columns:
            repeat_champs = champions_df.groupby(driver_col).size()
            max_wins = repeat_champs.max() if len(repeat_champs) > 0 else 1
        else:
            max_wins = 1
        st.metric("🔄 Most Championships", max_wins)
    
    st.divider()
    
    # =====================================================
    # CHAMPIONS TABLE
    # =====================================================
    
    st.markdown("### 📊 Championship History")
    
    # Select available columns safely
    available_cols = [col for col in ["SEASON", driver_col, "POINTS", "WINS", "PODIUMS", "POLE_POSITIONS"] 
                      if col and col in champions_df.columns]
    
    if len(available_cols) > 0:
        display_df = champions_df[available_cols].copy()
    else:
        display_df = champions_df.copy()
    
    # Dynamically rename columns based on what's available
    rename_map = {
        "SEASON": "Season",
        driver_col: "Champion" if driver_col else None,
        "POINTS": "Points",
        "WINS": "Wins",
        "PODIUMS": "Podiums",
        "POLE_POSITIONS": "Poles"
    }
    rename_map = {k: v for k, v in rename_map.items() if v is not None and k in display_df.columns}
    display_df = display_df.rename(columns=rename_map)
    
    # Create column config dynamically
    col_config = {
        "Season": st.column_config.NumberColumn("Season", format="%d"),
        "Champion": "Champion",
        "Points": st.column_config.NumberColumn("Championship Points", format="%.0f"),
        "Wins": st.column_config.NumberColumn("Wins", format="%d"),
        "Podiums": st.column_config.NumberColumn("Podiums", format="%d"),
        "Poles": st.column_config.NumberColumn("Pole Positions", format="%d"),
    }
    # Remove keys that don't exist in the dataframe
    col_config = {k: v for k, v in col_config.items() if k in display_df.columns}
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=col_config
    )
    
    st.divider()
    
    # =====================================================
    # CHAMPIONS BY FREQUENCY
    # =====================================================
    
    st.markdown("### 🏅 Multiple Champions")
    
    if driver_col and driver_col in champions_df.columns:
        champ_counts = champions_df.groupby(driver_col).size().reset_index(name="Championships")
        champ_counts = champ_counts.sort_values("Championships", ascending=False)
        
        if len(champ_counts[champ_counts["Championships"] > 1]) > 0:
            multi_champs = champ_counts[champ_counts["Championships"] > 1]
            
            for idx, row in multi_champs.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{row[driver_col]}**")
                with col2:
                    st.metric("Championships", row["Championships"], label_visibility="collapsed")
        else:
            st.info("All champions have won a single championship in this period.")
    else:
        st.warning("Cannot determine driver column in data.")
    
    st.divider()
    
    # =====================================================
    # RECENT CHAMPIONS
    # =====================================================
    
    st.markdown("### 🎯 Recent Champions")
    
    recent = champions_df.nlargest(5, "SEASON")
    
    if driver_col and driver_col in champions_df.columns:
        for idx, row in recent.iterrows():
            items = [("Driver", row[driver_col])]
            if "POINTS" in row:
                items.append(("Championship Points", f"{row['POINTS']:.0f}"))
            if "WINS" in row:
                items.append(("Wins", f"{int(row['WINS'])}"))
            if "PODIUMS" in row:
                items.append(("Podiums", f"{int(row['PODIUMS'])}"))
            
            info_card(
                title=f"🏆 {int(row['SEASON'])} Champion",
                items=items,
                icon="🏆"
            )
            st.write("")  # Add spacing
    else:
        st.warning("Cannot display recent champions - driver column not found.")

else:
    
    st.warning("""
    Champions data not available. This may indicate:
    - The data pipeline hasn't run yet
    - Driver standings table is not yet populated
    - Connection issue
    
    Please ensure the dbt pipeline has run successfully and the STG_DRIVER_STANDINGS table is populated.
    """)
    
    st.markdown("### 📊 Expected Data")
    st.info("""
    This page displays:
    - Season-by-season world champions
    - Championship points totals
    - Wins and podiums per champion
    - Historical champion analysis
    """)

st.divider()

# =====================================================
# FOOTER
# =====================================================

footer()