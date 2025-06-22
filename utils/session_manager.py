"""
Session Manager for Whiteout Survival Calculator
Handles Streamlit session state management.
"""

import streamlit as st
from typing import Dict, Any

def init_session_state():
    """Initialize all session state variables."""
    if 'auto_purchases' not in st.session_state:
        st.session_state.auto_purchases = None

    if 'manual_purchases' not in st.session_state:
        st.session_state.manual_purchases = None

    if 'training_params' not in st.session_state:
        st.session_state.training_params = {
            'general_speedups': 18000.0,
            'training_speedups': 1515.0,
            'days': 0,
            'hours': 4,
            'minutes': 50,
            'seconds': 0,
            'troops_per_batch': 426,
            'points_per_troop': 830.0
        }

    # Initialize Hall of Chiefs session state
    if 'hall_of_chiefs_construction_entries' not in st.session_state:
        st.session_state.hall_of_chiefs_construction_entries = []
    
    if 'hall_of_chiefs_research_entries' not in st.session_state:
        st.session_state.hall_of_chiefs_research_entries = []

def update_training_params(params: Dict[str, Any]):
    """Update training parameters in session state."""
    st.session_state.training_params.update(params)

def get_training_params() -> Dict[str, Any]:
    """Get current training parameters from session state."""
    return st.session_state.training_params

def update_purchases(auto_purchases=None, manual_purchases=None):
    """Update purchase data in session state."""
    if auto_purchases is not None:
        st.session_state.auto_purchases = auto_purchases
    if manual_purchases is not None:
        st.session_state.manual_purchases = manual_purchases

def get_purchases():
    """Get current purchase data from session state."""
    return st.session_state.auto_purchases, st.session_state.manual_purchases

def load_purchases_to_session(auto_path=None, manual_path=None):
    """Load purchases into session state."""
    from features.purchase_manager import load_purchases
    auto_purchases, manual_purchases = load_purchases(auto_path, manual_path)
    update_purchases(auto_purchases, manual_purchases)
    return auto_purchases, manual_purchases 