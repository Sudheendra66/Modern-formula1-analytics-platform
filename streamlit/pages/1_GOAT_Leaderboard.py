import streamlit as st
import pandas as pd

from snowflake_connection import get_connection

st.title("👑 GOAT Leaderboard")

conn = get_connection()

df = pd.read_sql("""
select *
from MART_DRIVER_ANALYTICS
order by GOAT_RANK
""", conn)

st.dataframe(df, use_container_width=True)

