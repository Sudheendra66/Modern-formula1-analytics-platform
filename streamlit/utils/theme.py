"""
Formula 1 Analytics Platform - Theme Configuration
Defines colors, styling, and visual constants for the entire application.
"""

import streamlit as st

# =====================================================
# COLOR PALETTE
# =====================================================

COLORS = {
    # Main colors
    "background": "#0E1117",
    "card_bg": "#1B2333",
    "sidebar_bg": "#151B26",
    "accent": "#E10600",
    "accent_hover": "#FF1A1A",
    
    # Semantic colors
    "success": "#00C853",
    "warning": "#FFA726",
    "error": "#E53935",
    
    # Medal colors
    "gold": "#FFD700",
    "silver": "#C0C0C0",
    "bronze": "#CD7F32",
    
    # Text colors
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B9C1",
    "text_muted": "#8B95A5",
    
    # Borders and dividers
    "border": "#2D3748",
    "divider": "#374151",
}

# =====================================================
# SPACING & SIZING
# =====================================================

SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
}

BORDER_RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
}

SHADOWS = {
    "sm": "0px 2px 4px rgba(0, 0, 0, 0.2)",
    "md": "0px 4px 12px rgba(0, 0, 0, 0.3)",
    "lg": "0px 8px 24px rgba(0, 0, 0, 0.4)",
}

# =====================================================
# PLOTLY LAYOUT TEMPLATE
# =====================================================

PLOTLY_LAYOUT = {
    "template": "plotly_dark",
    "paper_bgcolor": COLORS["background"],
    "plot_bgcolor": COLORS["background"],
    "font": dict(
        color=COLORS["text_primary"],
        family="Arial, sans-serif",
        size=12
    ),
    "hoverlabel": dict(
        bgcolor=COLORS["card_bg"],
        bordercolor=COLORS["accent"],
        font=dict(color=COLORS["text_primary"])
    ),
    "margin": dict(l=60, r=40, t=80, b=60),
}

# =====================================================
# LOAD THEME STYLING
# =====================================================

def load_theme():
    """
    Apply global theme styling to the Streamlit application.
    Call this function at the top of app.py and all page files.
    """
    
    st.set_page_config(
        page_title="🏎️ Formula 1 Analytics Platform",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(get_css(), unsafe_allow_html=True)


def get_css():
    """
    Return all custom CSS for the application.
    Centralizes styling to avoid duplication.
    """
    
    return f"""
    <style>
    
    /* ===== ROOT & GENERAL ===== */
    :root {{
        --bg-primary: {COLORS['background']};
        --bg-card: {COLORS['card_bg']};
        --bg-sidebar: {COLORS['sidebar_bg']};
        --accent: {COLORS['accent']};
        --text-primary: {COLORS['text_primary']};
        --text-secondary: {COLORS['text_secondary']};
        --gold: {COLORS['gold']};
        --silver: {COLORS['silver']};
        --bronze: {COLORS['bronze']};
        --border-radius: {BORDER_RADIUS['lg']};
    }}
    
    * {{
        box-sizing: border-box;
    }}
    
    /* ===== MAIN APP ===== */
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text_primary']};
    }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: {COLORS['background']};
    }}
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['sidebar_bg']};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {COLORS['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
        background-color: {COLORS['sidebar_bg']};
    }}
    
    .stSidebarContent {{
        background-color: {COLORS['sidebar_bg']};
    }}
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }}
    
    p, label, span, li {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    /* ===== BUTTONS ===== */
    .stButton > button {{
        background-color: {COLORS['accent']};
        color: {COLORS['text_primary']};
        border: none;
        border-radius: {BORDER_RADIUS['lg']};
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: {SHADOWS['md']};
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['accent_hover']};
        box-shadow: {SHADOWS['lg']};
        transform: translateY(-2px);
    }}
    
    /* ===== METRIC CARDS ===== */
    [data-testid="metric-container"] {{
        background-color: {COLORS['card_bg']};
        border-left: 4px solid {COLORS['accent']};
        border-radius: {BORDER_RADIUS['lg']};
        padding: 20px;
        box-shadow: {SHADOWS['md']};
        transition: all 0.3s ease;
    }}
    
    [data-testid="metric-container"]:hover {{
        box-shadow: {SHADOWS['lg']};
        transform: translateY(-4px);
        border-left-color: {COLORS['accent_hover']};
    }}
    
    [data-testid="metric-container"] * {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text_primary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: {BORDER_RADIUS['md']} !important;
        padding: 10px 12px !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['accent']} !important;
        box-shadow: 0 0 0 3px rgba(225, 6, 0, 0.1) !important;
    }}
    
    /* ===== SELECTBOX ===== */
    [data-testid="stSelectbox"] div div select {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text_primary']} !important;
        border-radius: {BORDER_RADIUS['md']} !important;
    }}
    
    /* ===== DATAFRAME ===== */
    [data-testid="stDataFrame"] {{
        background-color: {COLORS['card_bg']} !important;
        border-radius: {BORDER_RADIUS['lg']} !important;
        border: 1px solid {COLORS['border']} !important;
        overflow: hidden;
    }}
    
    [data-testid="stDataFrame"] table {{
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['card_bg']} !important;
    }}
    
    [data-testid="stDataFrame"] thead tr th {{
        background-color: {COLORS['accent']} !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 600 !important;
        border-bottom: 2px solid {COLORS['accent']} !important;
    }}
    
    [data-testid="stDataFrame"] tbody tr {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text_primary']} !important;
        border-bottom: 1px solid {COLORS['border']} !important;
    }}
    
    [data-testid="stDataFrame"] tbody tr:hover {{
        background-color: {COLORS['sidebar_bg']} !important;
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        color: {COLORS['text_primary']} !important;
        background-color: {COLORS['card_bg']};
        border-radius: {BORDER_RADIUS['md']};
        padding: 12px 16px !important;
        border: 1px solid {COLORS['border']};
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {COLORS['sidebar_bg']};
        border-color: {COLORS['accent']};
    }}
    
    .streamlit-expanderHeader svg {{
        color: {COLORS['accent']} !important;
    }}
    
    /* ===== DIVIDERS ===== */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['divider']}, transparent);
        margin: 24px 0;
    }}
    
    /* ===== TABS ===== */
    [data-testid="stTabs"] [role="tab"] {{
        color: {COLORS['text_secondary']} !important;
        border-bottom: 2px solid transparent;
        padding: 12px 24px;
    }}
    
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        color: {COLORS['accent']} !important;
        border-bottom: 2px solid {COLORS['accent']} !important;
    }}
    
    /* ===== COLUMNS ===== */
    .stColumn {{
        padding: 0 8px;
    }}
    
    /* ===== CAPTIONS & SMALL TEXT ===== */
    .stCaption {{
        color: {COLORS['text_muted']} !important;
        font-size: 0.85rem !important;
    }}
    
    /* ===== SUCCESS/ERROR MESSAGES ===== */
    .stSuccess {{
        background-color: rgba(0, 200, 83, 0.1) !important;
        border-left: 4px solid {COLORS['success']} !important;
    }}
    
    .stError {{
        background-color: rgba(229, 57, 53, 0.1) !important;
        border-left: 4px solid {COLORS['error']} !important;
    }}
    
    .stWarning {{
        background-color: rgba(255, 167, 38, 0.1) !important;
        border-left: 4px solid {COLORS['warning']} !important;
    }}
    
    .stInfo {{
        background-color: rgba(33, 150, 243, 0.1) !important;
        border-left: 4px solid #2196F3 !important;
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['card_bg']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['border']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['accent']};
    }}
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.3s ease-in-out;
    }}
    
    </style>
    """


def get_medal_color(rank: int) -> str:
    """
    Get medal color based on rank.
    
    Args:
        rank: Ranking position (1=gold, 2=silver, 3=bronze)
        
    Returns:
        Hex color code for the medal
    """
    if rank == 1:
        return COLORS["gold"]
    elif rank == 2:
        return COLORS["silver"]
    elif rank == 3:
        return COLORS["bronze"]
    else:
        return COLORS["accent"]


def format_number(value: float, decimal_places: int = 2) -> str:
    """Format number with consistent styling."""
    if isinstance(value, (int, float)):
        return f"{value:,.{decimal_places}f}"
    return str(value)
