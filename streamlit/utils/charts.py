"""
Formula 1 Analytics Platform - Chart Components
Reusable chart configurations for consistent Plotly styling.
"""

import plotly.graph_objects as go
import plotly.express as px
from utils.theme import COLORS, PLOTLY_LAYOUT


def get_base_layout(title: str = "", height: int = 500):
    """
    Get base layout configuration for Plotly charts.
    
    Args:
        title: Chart title
        height: Chart height in pixels
        
    Returns:
        Dictionary with layout configuration
    """
    layout = PLOTLY_LAYOUT.copy()
    layout["height"] = height
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(size=18, color=COLORS["text_primary"])
        )
    return layout


def styled_bar_chart(df, x, y, title="", color_scale="Reds", text_position="outside", height=500):
    """
    Create a styled bar chart.
    
    Args:
        df: DataFrame
        x: X-axis column
        y: Y-axis column
        title: Chart title
        color_scale: Plotly color scale
        text_position: Position of value labels
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=y,
        text=y,
        color_continuous_scale=color_scale,
        template="plotly_dark"
    )
    
    fig.update_traces(
        textposition=text_position,
        marker=dict(line=dict(color=COLORS["accent"], width=1))
    )
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    
    return fig


def styled_scatter_chart(df, x, y, size=None, color=None, hover_name="", title="", height=600):
    """
    Create a styled scatter chart.
    
    Args:
        df: DataFrame
        x: X-axis column
        y: Y-axis column
        size: Size column for bubble size
        color: Color column for color scale
        hover_name: Column for hover information
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover_name,
        color_continuous_scale="Turbo",
        template="plotly_dark",
        title=title
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(color=COLORS["card_bg"], width=1),
            opacity=0.8
        )
    )
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    
    return fig


def styled_line_chart(df, x, y, title="", height=500, color=None):
    """
    Create a styled line chart.
    
    Args:
        df: DataFrame
        x: X-axis column
        y: Y-axis column(s) - can be list
        title: Chart title
        height: Chart height
        color: Line color
        
    Returns:
        Plotly figure
    """
    if color is None:
        color = COLORS["accent"]
    
    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        template="plotly_dark"
    )
    
    fig.update_traces(
        line=dict(color=color, width=3),
        hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>"
    )
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    
    return fig


def styled_radar_chart(df, categories, values, title="", height=500):
    """
    Create a styled radar/spider chart.
    
    Args:
        df: DataFrame with data
        categories: List of category names
        values: Column name with values
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[values] if isinstance(values, str) else [row.get(v, 0) for v in values],
            theta=categories,
            fill='toself',
            name=row.get('name', f'Series {idx}'),
            line=dict(color=COLORS["accent"]),
            fillcolor=f"rgba(225, 6, 0, 0.3)"
        ))
    
    fig.update_layout(
        **get_base_layout(title, height),
        polar=dict(
            bgcolor=COLORS["card_bg"],
            radialaxis=dict(
                visible=True,
                range=[0, max(df[values]) if isinstance(values, str) else 100],
                tickfont=dict(color=COLORS["text_secondary"]),
                gridcolor=COLORS["border"]
            ),
            angularaxis=dict(
                tickfont=dict(color=COLORS["text_secondary"])
            )
        ),
        showlegend=True,
        legend=dict(
            x=1.1,
            y=1,
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    return fig


def styled_histogram(df, x, title="", nbins=30, height=500):
    """
    Create a styled histogram.
    
    Args:
        df: DataFrame
        x: Column to plot
        title: Chart title
        nbins: Number of bins
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = px.histogram(
        df,
        x=x,
        title=title,
        nbins=nbins,
        template="plotly_dark"
    )
    
    fig.update_traces(
        marker=dict(color=COLORS["accent"], line=dict(color=COLORS["card_bg"], width=1)),
        hovertemplate="<b>Range</b><br>%{x}<br>Count: %{y}<extra></extra>"
    )
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    
    return fig


def styled_box_plot(df, x, y, title="", height=500):
    """
    Create a styled box plot.
    
    Args:
        df: DataFrame
        x: X-axis column (categories)
        y: Y-axis column (values)
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = px.box(
        df,
        x=x,
        y=y,
        title=title,
        template="plotly_dark"
    )
    
    fig.update_traces(
        marker=dict(color=COLORS["accent"], opacity=0.7),
        line=dict(color=COLORS["accent"])
    )
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS["border"]
    )
    
    return fig


def styled_heatmap(z_data, x_labels, y_labels, title="", height=500):
    """
    Create a styled heatmap.
    
    Args:
        z_data: 2D array of values
        x_labels: X-axis labels
        y_labels: Y-axis labels
        title: Chart title
        height: Chart height
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        colorscale="Reds",
        colorbar=dict(
            thickness=20,
            tickfont=dict(color=COLORS["text_primary"]),
            tickcolor=COLORS["border"]
        ),
        hovertemplate="<b>%{x}</b><br><b>%{y}</b><br>Value: %{z:.2f}<extra></extra>"
    ))
    
    fig.update_layout(**get_base_layout(title, height))
    fig.update_xaxes(
        tickfont=dict(color=COLORS["text_primary"]),
        showgrid=False
    )
    fig.update_yaxes(
        tickfont=dict(color=COLORS["text_primary"]),
        showgrid=False
    )
    
    return fig
