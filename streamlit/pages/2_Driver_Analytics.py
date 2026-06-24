import streamlit as st
import pandas as pd

from snowflake_connection import get_connection

conn = get_connection()

df = pd.read_sql("""
select *
from MART_DRIVER_ANALYTICS
""", conn)

st.title("📊 Driver Analytics")

driver = st.selectbox(
    "Choose Driver",
    sorted(df["DRIVER_NAME"].dropna().unique())
)

selected = df[df["DRIVER_NAME"] == driver]

col1,col2,col3 = st.columns(3)

col1.metric(
    "Career Points",
    round(selected["CAREER_POINTS"].iloc[0],2)
)

col2.metric(
    "Wins",
    int(selected["WINS"].iloc[0])
)

col3.metric(
    "Podiums",
    int(selected["PODIUMS"].iloc[0])
)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Win Rate %",
    round(selected["WIN_RATE"].iloc[0],2)
)

col2.metric(
    "Podium Rate %",
    round(selected["PODIUM_RATE"].iloc[0],2)
)

col3.metric(
    "GOAT Score",
    round(selected["GOAT_SCORE"].iloc[0],2)
)