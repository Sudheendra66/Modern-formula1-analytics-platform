"""
Formula 1 Analytics Platform - Card Components
Simple Streamlit-native components for reliable dashboard rendering.
"""

import streamlit as st


def _safe_value(value):
    return "N/A" if value is None else value


def metric_card(label: str, value: str, icon: str = "", change: str = "", color: str = None):
    """Display a metric using Streamlit's native metric component."""
    st.metric(label=f"{icon} {label}".strip(), value=_safe_value(value), delta=change or None)


def kpi_row(kpis: list):
    """Display a row of KPI metrics."""
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            metric_card(
                label=kpi.get("label", ""),
                value=kpi.get("value", "N/A"),
                icon=kpi.get("icon", ""),
            )


def medal_card(rank: int, driver_name: str, score: float, wins: int, podiums: int, points: float, medal_color: str = None):
    """Display a clean top-three driver card with native Streamlit elements."""
    rank_label = "1st" if rank == 1 else "2nd" if rank == 2 else "3rd"

    with st.container(border=True):
        st.markdown(f"### {rank_label} | {driver_name}")
        st.metric("GOAT Score", f"{score:.2f}")
        st.markdown(
            f"""
            | Wins | Podiums | Points |
            |---:|---:|---:|
            | {int(wins)} | {int(podiums)} | {points:,.0f} |
            """
        )


def info_card(title: str, items: list, icon: str = ""):
    """Display a simple information card using native Streamlit layout."""
    with st.container(border=True):
        st.markdown(f"#### {icon} {title}".strip())
        for label, value in items:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(label)
            with col2:
                st.write(f"**{_safe_value(value)}**")


def hero_section(title: str, subtitle: str, icon: str = ""):
    """Display a simple page header."""
    st.title(f"{icon} {title}".strip())
    if subtitle:
        st.caption(subtitle)
    st.divider()


def footer():
    """Display a simple footer."""
    st.divider()
    st.caption("Formula 1 Analytics Platform | Powered by Snowflake, dbt, Fivetran Connector SDK, and Streamlit")


def progress_bar(label: str, value: float, max_value: float = 100, color: str = None):
    """Display a native progress bar with value text."""
    value = float(value or 0)
    max_value = float(max_value or 0)
    ratio = min(max(value / max_value, 0), 1) if max_value > 0 else 0

    st.write(f"**{label}**")
    st.progress(ratio)
    st.caption(f"{value:.2f} / {max_value:.2f}")