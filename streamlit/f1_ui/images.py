"""
Formula 1 Analytics Platform - Image Utilities
Utilities for loading and displaying images with fallback support.
"""

import os
from pathlib import Path
import streamlit as st


# Base image directories
IMAGES_BASE_DIR = Path(__file__).parent.parent / "assets" / "images"
DRIVER_IMAGES_DIR = IMAGES_BASE_DIR / "drivers"
TEAM_IMAGES_DIR = IMAGES_BASE_DIR / "teams"
CIRCUIT_IMAGES_DIR = IMAGES_BASE_DIR / "circuits"

# Supported image formats
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".gif", ".webp"]


def get_driver_image(driver_name: str, default_emoji: str = "🏎️"):
    """
    Get driver image path or return emoji placeholder.
    
    Args:
        driver_name: Driver name
        default_emoji: Emoji to display if image not found
        
    Returns:
        Tuple of (image_path or None, emoji)
    """
    if not driver_name:
        return None, default_emoji
    
    # Sanitize driver name for filename
    safe_name = driver_name.lower().replace(" ", "_").replace("-", "_")
    
    # Check for image file
    for ext in SUPPORTED_FORMATS:
        image_path = DRIVER_IMAGES_DIR / f"{safe_name}{ext}"
        if image_path.exists():
            return str(image_path), "🏎️"
    
    return None, "👤"


def get_team_image(team_name: str, default_emoji: str = "🏁"):
    """
    Get team image path or return emoji placeholder.
    
    Args:
        team_name: Team name
        default_emoji: Emoji to display if image not found
        
    Returns:
        Tuple of (image_path or None, emoji)
    """
    if not team_name:
        return None, default_emoji
    
    # Sanitize team name for filename
    safe_name = team_name.lower().replace(" ", "_").replace("-", "_")
    
    # Check for image file
    for ext in SUPPORTED_FORMATS:
        image_path = TEAM_IMAGES_DIR / f"{safe_name}{ext}"
        if image_path.exists():
            return str(image_path), "🏁"
    
    return None, "🏢"


def get_circuit_image(circuit_name: str, default_emoji: str = "🏁"):
    """
    Get circuit image path or return emoji placeholder.
    
    Args:
        circuit_name: Circuit name
        default_emoji: Emoji to display if image not found
        
    Returns:
        Tuple of (image_path or None, emoji)
    """
    if not circuit_name:
        return None, default_emoji
    
    # Sanitize circuit name for filename
    safe_name = circuit_name.lower().replace(" ", "_").replace("-", "_")
    
    # Check for image file
    for ext in SUPPORTED_FORMATS:
        image_path = CIRCUIT_IMAGES_DIR / f"{safe_name}{ext}"
        if image_path.exists():
            return str(image_path), "🏁"
    
    return None, "🛣️"


def display_image(image_path: str, width: int = 100, caption: str = ""):
    """
    Display an image in Streamlit.
    
    Args:
        image_path: Path to image file
        width: Image width
        caption: Optional caption
    """
    if image_path and os.path.exists(image_path):
        st.image(image_path, width=width, caption=caption)
    else:
        st.info(f"Image not found: {image_path}")


def get_all_available_drivers():
    """
    Get list of all drivers with available images.
    
    Returns:
        List of driver names (from filenames)
    """
    drivers = []
    if DRIVER_IMAGES_DIR.exists():
        for file in DRIVER_IMAGES_DIR.iterdir():
            if file.is_file() and file.suffix in SUPPORTED_FORMATS:
                drivers.append(file.stem.replace("_", " ").title())
    return sorted(drivers)


def get_all_available_teams():
    """
    Get list of all teams with available images.
    
    Returns:
        List of team names (from filenames)
    """
    teams = []
    if TEAM_IMAGES_DIR.exists():
        for file in TEAM_IMAGES_DIR.iterdir():
            if file.is_file() and file.suffix in SUPPORTED_FORMATS:
                teams.append(file.stem.replace("_", " ").title())
    return sorted(teams)


def get_all_available_circuits():
    """
    Get list of all circuits with available images.
    
    Returns:
        List of circuit names (from filenames)
    """
    circuits = []
    if CIRCUIT_IMAGES_DIR.exists():
        for file in CIRCUIT_IMAGES_DIR.iterdir():
            if file.is_file() and file.suffix in SUPPORTED_FORMATS:
                circuits.append(file.stem.replace("_", " ").title())
    return sorted(circuits)


def ensure_image_directories():
    """Ensure all image directories exist."""
    DRIVER_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    TEAM_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    CIRCUIT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
