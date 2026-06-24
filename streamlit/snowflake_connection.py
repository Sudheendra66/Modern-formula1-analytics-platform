import streamlit as st
import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["account"],
        user=st.secrets["user"],
        password=st.secrets["password"],
        warehouse=st.secrets["warehouse"],
        database=st.secrets["database"],
        schema=st.secrets["schema"],
        role=st.secrets["role"]
    )